import enum
import scrapy
import sqlite3

class ImigresenSpider(scrapy.Spider):
    name = 'imigresen'

    def start_requests(self):
        connection = sqlite3.connect('imigresen.db')
        cursor = connection.cursor()

        # Empty the branch table
        cursor.execute("DELETE FROM branch")
        connection.commit()
        # Empty the services table
        cursor.execute("DELETE FROM services")
        connection.commit()
        # Empty the slot table
        cursor.execute("DELETE FROM slot")
        connection.commit()
        # Empty the date table
        cursor.execute("DELETE FROM date")
        connection.commit()

        # Start from state table
        cursor.execute("SELECT * FROM state")
        rows = cursor.fetchall()

        for row in rows:
            url = 'http://sto.imi.gov.my/sto/cawangan.php?idjim=' + str(row[0])
            yield scrapy.Request(url, self.parse_branch, meta={'state_id': row[0]})

        connection.close()

    def parse_branch(self, response):
        connection = sqlite3.connect('imigresen.db')
        cursor = connection.cursor()

        # Branch table
        for option in response.xpath('//option'):
            value = option.xpath('@value').get()
            state_id = response.meta.get('state_id')
            text = option.xpath('text()').get()
            if value is not None:
                cursor.execute("INSERT INTO branch VALUES (?, ?, ?)", (value, state_id, text))
                connection.commit()
                url = 'http://sto.imi.gov.my/sto/urusniaga.php?jenis=1&idjim=' + str(value)
                yield response.follow(url, self.parse_services, meta={'branch_id': value})

        connection.close()

    def parse_services(self, response):
        connection = sqlite3.connect('imigresen.db')
        cursor = connection.cursor()

        # Services table
        for option in response.xpath('//option'):
            value = option.xpath('@value').get()
            branch_id = response.meta.get('branch_id')
            text = option.xpath('text()').get()
            if value is not None:
                cursor.execute("INSERT INTO services VALUES (?, ?, ?)", (value, branch_id, text))
                connection.commit()
                url = 'http://sto.imi.gov.my/sto/slotappt.php?trxn=' + str(value)
                yield response.follow(url, self.parse_slot, meta={'service_id': value})

        connection.close()

    def parse_slot(self, response):
        connection = sqlite3.connect('imigresen.db')
        cursor = connection.cursor()

        # Slot table
        options = response.xpath('//option')
        list_value = []
        list_text = []
        for option in options:
            value = option.xpath('@value').get()
            text = option.xpath('text()').get()
            if value is not None and value not in list_value:
                list_value.append(value)
                list_text.append(text)

        for index, element in enumerate(list_value):
            value = element
            service_id = response.meta.get('service_id')
            text = list_text[index]
            cursor.execute("INSERT INTO slot VALUES (?, ?, ?)", (value, service_id, text))
            connection.commit()
            url = 'http://sto.imi.gov.my/sto/availabledate.php?slotku=' + str(value) + '&urusku=' + str(service_id)
            yield response.follow(url, self.parse_date, meta={'service_id': service_id, 'slot_id': value})

        connection.close()

    def parse_date(self, response):
        connection = sqlite3.connect('imigresen.db')
        cursor = connection.cursor()

        # Date table
        for option in response.xpath('//option'):
            value = option.xpath('@value').get()
            slot_id = response.meta.get('slot_id')
            service_id = response.meta.get('service_id')
            text = option.xpath('text()').get()
            if value is not None:
                cursor.execute("INSERT INTO date VALUES (?, ?, ?, ?)", (value, slot_id, service_id, text))
                connection.commit()

        connection.close()