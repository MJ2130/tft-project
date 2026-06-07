# tft-project

## 비교 분석을 위해 사용한 spark 코드
1. (하위권 티어 레벨별 평균 순위)

>>> spark.sql("""
... SELECT
... level,
... ROUND(AVG(placement),2) avg_place,
... ROUND(AVG(top4)*100,2) top4_rate,
... COUNT(*) cnt
... FROM low_tft
... GROUP BY level
... ORDER BY level
... """).show()
+-----+---------+---------+----+
|level|avg_place|top4_rate| cnt|
+-----+---------+---------+----+
|    4|      5.6|    33.33|  15|
|    5|     7.66|     2.47| 162|
|    6|      6.8|     7.68| 482|
|    7|     5.77|     23.3|1571|
|    8|     4.84|    43.71|3345|
|    9|     3.52|     69.5|2987|
|   10|     2.32|    88.66| 882|
+-----+---------+---------+----+


2.(상위권 티어 레벨별 평균순위)
>>> spark.sql("""
... SELECT
... level,
... ROUND(AVG(placement),2) avg_place,
... ROUND(AVG(top4)*100,2) top4_rate,
... COUNT(*) cnt
... FROM high_tft
... GROUP BY level
... ORDER BY level
... """).show()
+-----+---------+---------+----+
|level|avg_place|top4_rate| cnt|
+-----+---------+---------+----+
|    4|      8.0|      0.0|   1|
|    5|     7.94|      0.0|  33|
|    6|     7.21|     3.03|  66|
|    7|     5.86|     21.8| 743|
|    8|      5.2|     36.7|2098|
|    9|      4.1|    58.59|2676|
|   10|     2.08|    93.18| 718|
+-----+---------+---------+----+

3. (저티어 리롤덱, 운영덱 비율)
>>> spark.sql("""
... SELECT
... CASE
... WHEN champ_details LIKE '%:3%' THEN 'STAR3'
... ELSE 'NO_STAR3'
... END AS star_group,
... ROUND(AVG(placement),2) AS avg_place,
... ROUND(AVG(top4)*100,2) AS top4_rate,
... COUNT(*) AS cnt
... FROM low_tft
... GROUP BY
... CASE
... WHEN champ_details LIKE '%:3%' THEN 'STAR3'
... ELSE 'NO_STAR3'
... END
... """).show()
+----------+---------+---------+----+
|star_group|avg_place|top4_rate| cnt|
+----------+---------+---------+----+
|     STAR3|     3.94|    60.07|4663|
|  NO_STAR3|     5.03|    40.39|4781|
+----------+---------+---------+----+

4. (상위권 티어 리롤덱, 운영덱 비율)
>>> spark.sql("""
... SELECT
... CASE
... WHEN champ_details LIKE '%:3%' THEN 'STAR3'
... ELSE 'NO_STAR3'
... END AS star_group,
... ROUND(AVG(placement),2) AS avg_place,
... ROUND(AVG(top4)*100,2) AS top4_rate,
... COUNT(*) AS cnt
... FROM high_tft
... GROUP BY
... CASE
... WHEN champ_details LIKE '%:3%' THEN 'STAR3'
... ELSE 'NO_STAR3'
... END
... """).show()
+----------+---------+---------+----+
|star_group|avg_place|top4_rate| cnt|
+----------+---------+---------+----+
|     STAR3|     4.09|    57.09|2664|
|  NO_STAR3|     4.79|    44.95|3671|
+----------+---------+---------+----+

