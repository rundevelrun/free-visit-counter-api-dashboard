create table sites
(
    id              integer   default nextval('site_id_seq'::regclass) not null
        constraint site_pkey
            primary key,
    domain          varchar(255)                                       not null
        constraint site_domain_key
            unique,
    total_count     integer   default 0,
    today_count     integer   default 0,
    last_visit_date date,
    created_at      timestamp default CURRENT_TIMESTAMP
);

alter table sites
    owner to niphyang_dev;

create index idx_site_domain
    on sites (domain);

create table visit_log
(
    id        serial
        primary key,
    site_id   integer not null
        references sites,
    timestamp timestamp default CURRENT_TIMESTAMP
);

alter table visit_log
    owner to niphyang_dev;

create index idx_visit_log_site_id
    on visit_log (site_id);

create index idx_visit_log_timestamp
    on visit_log (timestamp);
