# Crawl online appointment dates for Jabatan Imigresen Malaysia

This is a very basic Python scrapy crawling program written for my personal use and education purposes. It is to gather sufficient information for me to decide my desired passport renewal appointment date.

## Background

The world has changed ever since COVID-19 visited Malaysia in March 2020. You need to book an appointment online for almost every over-the-counter service in the current post-pandemic era. Some did a fantastic job with their online appointment booking system, but some did otherwise.

It is the same for Malaysia passport over-the-counter renewal, which online appointment is mandatory as well. Online passport renewal is not an option for me due to some restrictions.

The following screenshot shows the current online appointment system where you need to perform the selection by clicking the dropdown from top to bottom which date is the last dropdown
![Sistem Temujanji Online](https://user-images.githubusercontent.com/532986/163326863-ca3267aa-1ca8-42dd-90ca-96e67dba562e.png)

## Assumptions from my discovery

-   Different branch offers different set of services
    -   Services are not standardized
    -   It seems like it is up to the branch to key-in and decide
-   State id, branch id, service id, and slot id are all unique for whole Malaysia
-   There is a duplicate value issue for the slot dropdown
-   Possible passport renewal service id = 190, 486, 487, 488, 491, 500, 510, 523, 526, 529, 539, 541, 542, 544, 554, 562, 563, 564, 569, 588, 589, 609, 624, 630, 672, 673, 696, 709, 719, 721, 722, 725, 736, 749, 761, 766, 786, 800, 874, 893, 902, 904, 910, 911, 914, 949, 951, 956, 959, 966, 972, 975, 978, 986, 988, 996, 1011, 1012, 1034, 1040, 1041, 1091, 1092, 1096, 1110

## My current setup

-   Python v3.9.7 (Anaconda v4.11.0)
-   Scrapy v2.6.1
-   SQLite v3.36.0 (macOS built-in)
-   TablePlus v3.12.0

## To run

```bash
    git clone git@github.com:cheetooh/scrapy-imigresen.git
    cd scrapy-imigresen/imigresenscraper
    scrapy crawl imigresen
```

## The result

To look for earliest available weekend dates for UTC that is not located in Perlis, Miri, Kota Kinabalu, Tawau and Keningau

```sql
SELECT
	*
FROM
	'date' AS a
	LEFT JOIN slot AS b ON b.id = a.slot_id
	LEFT JOIN services AS c ON c.id = a.service_id
	LEFT JOIN branch AS d ON d.id = c.branch_id
WHERE
	a.service_id IN(190, 486, 487, 488, 491, 500, 510, 523, 526, 529, 539, 541, 542, 544, 554, 562, 563, 564, 569, 588, 589, 609, 624, 630, 672, 673, 696, 709, 719, 721, 722, 725, 736, 749, 761, 766, 786, 800, 874, 893, 902, 904, 910, 911, 914, 949, 951, 956, 959, 966, 972, 975, 978, 986, 988, 996, 1011, 1012, 1034, 1040, 1041, 1091, 1092, 1096, 1110)
	AND d.name LIKE 'UTC%'
	AND(a.name LIKE '%SABTU%'
		OR a.name LIKE '%AHAD%')
	AND c.branch_id NOT IN(168, 197, 161, 196, 112, 167)
ORDER BY
	a. "date"
```

![SQL result](https://user-images.githubusercontent.com/532986/163334247-f1c5a361-04f3-43bc-a36b-5d09a1fee984.png)
