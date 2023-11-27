/* Table creation*/
/*==========================================================================*/
create table ca_voclinks
(
   voclink_id                       int unsigned               not null AUTO_INCREMENT,
   parent_id                      int unsigned,
   locale_id                      smallint unsigned,
   type_id                        int unsigned                   null,
   source_id                      int unsigned,
   hierarchy_id                   int unsigned                   not null,
   idno                           varchar(255)                   not null,
   idno_sort                      varchar(255)                   not null,
   idno_sort_num                  bigint                         not null default 0,
   is_template                    tinyint unsigned               not null default 0,
   commenting_status              tinyint unsigned               not null default 0,
   tagging_status                 tinyint unsigned               not null default 0,
   rating_status                  tinyint unsigned               not null default 0,
   view_count                     int unsigned                   not null default 0,
   source_info                    longtext                       not null,
   lifespan_sdate                 decimal(30,20),
   lifespan_edate                 decimal(30,20),
   access                         tinyint unsigned               not null default 0,
   status                         tinyint unsigned               not null default 0,
   deleted                        tinyint unsigned               not null default 0,
   hier_left                      decimal(30,20)                 not null,
   hier_right                     decimal(30,20)                 not null,
   `rank`                           int unsigned                   not null default 0,
   floorplan                      longblob                       not null,
   submission_user_id               int unsigned                   null,
   submission_group_id            int unsigned                   null,
   submission_status_id              int unsigned                   null,
   submission_via_form            varchar(100)                   null,
   submission_session_id          int unsigned                   null,
   
   primary key (voclink_id),
   constraint fk_ca_voclinks_source_id foreign key (source_id)
      references ca_list_items (item_id) on delete restrict on update restrict,
      
   constraint fk_ca_voclinks_hierarchy_id foreign key (hierarchy_id)
      references ca_list_items (item_id) on delete restrict on update restrict,
      
   constraint fk_ca_voclinks_type_id foreign key (type_id)
      references ca_list_items (item_id) on delete restrict on update restrict,
      
   constraint fk_ca_voclinks_locale_id foreign key (locale_id)
      references ca_locales (locale_id) on delete restrict on update restrict,
      
   constraint fk_ca_voclinks_parent_id foreign key (parent_id)
      references ca_voclinks (voclink_id) on delete restrict on update restrict,
   
   constraint fk_ca_voclinks_submission_user_id foreign key (submission_user_id)
      references ca_users (user_id) on delete restrict on update restrict,

   constraint fk_ca_voclinks_submission_group_id foreign key (submission_group_id)
      references ca_user_groups (group_id) on delete restrict on update restrict,

   constraint fk_ca_voclinks_submission_status_id foreign key (submission_status_id)
      references ca_list_items (item_id) on delete restrict on update restrict,

   constraint fk_ca_voclinks_submission_session_id foreign key (submission_session_id)
      references ca_media_upload_sessions(session_id) on delete restrict on update restrict
) engine=innodb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

create index i_hierarchy_id on ca_voclinks(hierarchy_id);
create index i_type_id on ca_voclinks(type_id);
create index i_idno on ca_voclinks(idno);
create index i_idno_sort on ca_voclinks(idno_sort);
create index i_idno_sort_num on ca_voclinks(idno_sort_num);
create index i_locale_id on ca_voclinks(locale_id);
create index i_source_id on ca_voclinks(source_id);
create index i_life_sdatetime on ca_voclinks(lifespan_sdate);
create index i_life_edatetime on ca_voclinks(lifespan_edate);
create index i_parent_id on ca_voclinks(parent_id);
create index i_hier_left on ca_voclinks(hier_left);
create index i_hier_right on ca_voclinks(hier_right);
create index i_view_count on ca_voclinks(view_count);
create index i_voclink_filter on ca_voclinks(voclink_id, deleted, access); 
create index i_submission_user_id on ca_voclinks(submission_user_id);
create index i_submission_group_id on ca_voclinks(submission_group_id);
create index i_submission_status_id on ca_voclinks(submission_status_id);
create index i_submission_via_form on ca_voclinks(submission_via_form);
create index i_submission_session_id on ca_voclinks(submission_session_id);


/*==========================================================================*/
/*==========================================================================*/
create table ca_voclink_labels
(
   label_id                       int unsigned               not null AUTO_INCREMENT,
   voclink_id                       int unsigned               not null,
   locale_id                      smallint unsigned              not null,
   type_id                        int unsigned                   null,
   name                           varchar(255)                   not null,
   name_sort                      varchar(255)                   not null,
   source_info                    longtext                       not null,
   is_preferred                   tinyint unsigned               not null,
   sdatetime                      decimal(30,20),
   edatetime                      decimal(30,20),
   access                         tinyint unsigned               not null default 0,
   
   primary key (label_id),
   constraint fk_ca_voclink_labels_type_id foreign key (type_id)
      references ca_list_items (item_id) on delete restrict on update restrict,
   constraint fk_ca_voclink_labels_locale_id foreign key (locale_id)
      references ca_locales (locale_id) on delete restrict on update restrict,
   constraint fk_ca_voclink_labels_voclink_id foreign key (voclink_id)
      references ca_voclinks (voclink_id) on delete restrict on update restrict
) engine=innodb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

create index i_voclink_id on ca_voclink_labels(voclink_id);
create index i_name on ca_voclink_labels(name(128));
create index i_name_sort on ca_voclink_labels(name_sort(128));
create unique index u_all on ca_voclink_labels
(
   voclink_id,
   name,
   type_id,
   locale_id
);
create index i_locale_id on ca_voclink_labels(locale_id);
create index i_type_id on ca_voclink_labels(type_id);
create index i_effective_date ON ca_voclink_labels(sdatetime, edatetime);


/*==========================================================================*/
/*==========================================================================*/
create table ca_objects_x_voclinks
(
   relation_id                    int unsigned                   not null AUTO_INCREMENT,
   voclink_id                       int unsigned               not null,
   object_id                      int unsigned               not null,
   type_id                        smallint unsigned              not null,
   source_info                    longtext                       not null,
   sdatetime                      decimal(30,20),
   edatetime                      decimal(30,20),
   label_left_id                  int unsigned                   null,
   label_right_id                 int unsigned                   null,
   `rank`                           int unsigned                   not null default 0,
   primary key (relation_id),
   constraint fk_ca_objects_x_voclinks_type_id foreign key (type_id)
      references ca_relationship_types (type_id) on delete restrict on update restrict,
      
   constraint fk_ca_objects_x_voclinks_voclink_id foreign key (voclink_id)
      references ca_voclinks (voclink_id) on delete restrict on update restrict,
      
   constraint fk_ca_objects_x_voclinks_object_id foreign key (object_id)
      references ca_objects (object_id) on delete restrict on update restrict,
      
   constraint fk_ca_objects_x_voclinks_label_left_id foreign key (label_left_id)
      references ca_object_labels (label_id) on delete restrict on update restrict,
      
   constraint fk_ca_objects_x_voclinks_label_right_id foreign key (label_right_id)
      references ca_voclink_labels (label_id) on delete restrict on update restrict
) engine=innodb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

create index i_voclink_id on ca_objects_x_voclinks(voclink_id);
create index i_object_id on ca_objects_x_voclinks(object_id);
create index i_type_id on ca_objects_x_voclinks(type_id);
create unique index u_all on ca_objects_x_voclinks
(
   voclink_id,
   object_id,
   type_id,
   sdatetime,
   edatetime
);
create index i_label_left_id on ca_objects_x_voclinks(label_left_id);
create index i_label_right_id on ca_objects_x_voclinks(label_right_id);


/*==========================================================================*/