CREATE TABLE homePage (
    dlTimestamp     varchar(26) NOT NULL,
    postTime        varchar(20) NOT NULL,
    relTime         varchar(26) NOT NULL,
    headLine        varchar(180) NOT NULL,
    postsBy         varchar(40),
    postsByLink     varchar(48),
    headLineLink    varchar(180) NOT NULL,
    PRIMARY KEY(headLineLink)
    ) ENGINE = InnoDB CHAR SET=utf8;