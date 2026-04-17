-- ============================================================
-- LA County Sheriff - Traffic Collision Database
-- ============================================================

CREATE DATABASE SheriffIncidents;
GO
USE SheriffIncidents;
GO

-- ============================================================
-- DIMENSION TABLES (must be created before fact_report)
-- ============================================================

CREATE TABLE dim_area (
    area_id     INT         PRIMARY KEY,
    area_name   VARCHAR(200) NOT NULL
);

CREATE TABLE dim_crime (
    crime_code  INT         PRIMARY KEY,
    crime_name  VARCHAR(200) NOT NULL
);

CREATE TABLE dim_mo (
    mo_code     INT         PRIMARY KEY,
    mo_name     VARCHAR(500) NULL
);

CREATE TABLE dim_descent (
    descent_code    CHAR(1)         PRIMARY KEY,
    descent_name    VARCHAR(200)   NOT NULL
);

CREATE TABLE dim_sex (
    sex_code    CHAR(1)         PRIMARY KEY,
    sex_name    VARCHAR(200)   NOT NULL
);

CREATE TABLE dim_premise (
    premise_code    INT         PRIMARY KEY,
    premise_name    VARCHAR(200) NULL
);

-- ============================================================
-- FACT TABLE
-- ============================================================

CREATE TABLE fact_report (
    report_number   BIGINT      PRIMARY KEY,
    date_reported   DATE        NOT NULL,
    date_occurred   DATE        NOT NULL,
    time_occurred   TIME        NULL,
    area_id         INT         NOT NULL,
    crime_code      INT         NOT NULL,
    victim_age      TINYINT     NULL,
    victim_sex      CHAR(1)     NULL,
    victim_descent  CHAR(1)     NULL,
    premise_code    INT         NULL,
    address         VARCHAR(500) NULL,
    cross_street    VARCHAR(500) NULL,
    latitude        DECIMAL(9,6)   NULL,
    longitude        DECIMAL(9,6)   NULL,

    CONSTRAINT fk_area          FOREIGN KEY (area_id)       REFERENCES dim_area(area_id),
    CONSTRAINT fk_crime         FOREIGN KEY (crime_code)    REFERENCES dim_crime(crime_code),
    CONSTRAINT fk_sex           FOREIGN KEY (victim_sex)    REFERENCES dim_sex(sex_code),
    CONSTRAINT fk_descent       FOREIGN KEY (victim_descent)REFERENCES dim_descent(descent_code),
    CONSTRAINT fk_premise       FOREIGN KEY (premise_code)  REFERENCES dim_premise(premise_code)
);

-- ============================================================
-- BRIDGE TABLE
-- ============================================================

CREATE TABLE bridge_report_mo_code (
    report_number   BIGINT  NOT NULL,
    mo_code         INT     NOT NULL,

    CONSTRAINT pk_bridge        PRIMARY KEY (report_number, mo_code),
    CONSTRAINT fk_bridge_report FOREIGN KEY (report_number) REFERENCES fact_report(report_number),
    CONSTRAINT fk_bridge_mo     FOREIGN KEY (mo_code)       REFERENCES dim_mo(mo_code)
);

-- ============================================================
-- STAGING TABLE
-- ============================================================

CREATE TABLE stg_mo_raw(
	[report_number] [bigint] NOT NULL,
	[mo_codes_raw] [varchar](1000) NULL
);


-- ============================================================
-- AUDIT TABLE
-- ============================================================

CREATE TABLE dbo.etl_audit_log (
    audit_id        BIGINT          IDENTITY(1,1)   PRIMARY KEY,
    package_name    VARCHAR(100)    NOT NULL,
    error_code      INT             NULL,
    error_message   VARCHAR(MAX)    NULL,
    time_of_failure DATETIME        DEFAULT GETDATE(),
    error_location  VARCHAR(100)    NULL,
    data            VARCHAR(MAX)    NULL
);