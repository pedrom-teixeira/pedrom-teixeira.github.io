import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, to_date



sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite","CORRECTED")

df_preprocessed = spark.read.csv("s3://atomicpersonal-datalake/covid_raw_data/INFLUD22-04-01-2022.csv", sep =';', header = True)
df_final=df_preprocessed.where((col("RES_AN") == 1) & ((col("AN_SARS2") == 1) | (col("PCR_SARS2") == 1))) \
.select(to_date(col("DT_NOTIFIC"),"dd/MM/yyyy").alias("DT_NOTIFIC"),
	to_date(col("DT_SIN_PRI"),"dd/MM/yyyy").alias("DT_SIN_PRI"),
	col("EVOLUCAO"),
	to_date(col("DT_EVOLUCA"),"dd/MM/yyyy").alias("DT_EVOLUCA"),
	col("RES_AN"),
    col("AN_SARS2"),
	col("PCR_SARS2"),
	col("CS_ZONA"),
	col("VACINA_COV"),
	to_date(col("DOSE_1_COV"),"dd/MM/yyyy").alias("DOSE_1_COV"),
	to_date(col("DOSE_2_COV"),"dd/MM/yyyy").alias("DOSE_2_COV"),
	col("PUERPERA"),
	col("CARDIOPATI"),
	col("HEMATOLOGI"),
	col("SIND_DOWN"),
	col("HEPATICA"),
	col("ASMA"),
	col("DIABETES"),
	col("NEUROLOGIC"),
	col("PNEUMOPATI"),
	col("IMUNODEPRE"),
	col("RENAL"),
	col("OBESIDADE"),
	col("OUT_MORBI"),
	col("HOSPITAL"),
	col("FEBRE"),
	col("TOSSE"),
	col("GARGANTA"),
	col("DISPNEIA"),
	col("DESC_RESP"),
	col("SATURACAO"),
	col("DIARREIA"),
	col("VOMITO"),
	col("DOR_ABD"),
	col("FADIGA"),
	col("PERD_OLFT"),
	col("PERD_PALA"),
	col("OUTRO_SIN")) \
.write.parquet("s3://atomicpersonal-datawarehouse/covid_prepared_data/covid_raw_data.parquet")
