insert into process_definitions (name) values ('paprika-purge-log');
insert into process_definitions (name) values ('paprika-purge-log-exceptions');

insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-log'), 'state.processing');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-log'), 'purge.log');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-log'), 'state.processed');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-log-exceptions'), 'state.failed');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log','state.processing'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log','state.processing'), 'state', 'PROCESSING');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log','purge.log'), 'action', 'paprika.actions.events.PurgeLog.PurgeLog');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log','purge.log'), 'days', '60');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log','state.processed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log','state.processed'), 'state', 'PROCESSED');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log-exceptions','state.failed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-log-exceptions','state.failed'), 'state', 'FAILED');

insert into scheduled_events(name, repetition, expected, active, pdn_id, e_pdn_id) values ('paprika-purge-log', 'DAYS', STR_TO_DATE('10-10-2016 23:00:00','%m-%d-%Y %H:%i:%s'), 1, get_process_definition_id('paprika-purge-log'), get_process_definition_id('paprika-purge-log-exceptions'));