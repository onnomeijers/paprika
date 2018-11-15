insert into process_definitions (name) values ('paprika-purge-chunks');
insert into process_definitions (name) values ('paprika-purge-chunks-exceptions');

insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-chunks'), 'state.processing');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-chunks'), 'purge.chunks');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-chunks'), 'state.processed');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-chunks-exceptions'), 'state.failed');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks','state.processing'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks','state.processing'), 'state', 'PROCESSING');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks','purge.chunks'), 'action', 'paprika.actions.events.PurgeChunks.PurgeChunks');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks','purge.chunks'), 'days', '60');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks','state.processed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks','state.processed'), 'state', 'PROCESSED');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks-exceptions','state.failed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-chunks-exceptions','state.failed'), 'state', 'FAILED');

insert into scheduled_events(name, repetition, expected, active, pdn_id, e_pdn_id) values ('paprika-purge-chunks', 'DAYS', STR_TO_DATE('10-10-2016 23:00:00','%m-%d-%Y %H:%i:%s'), 1, get_process_definition_id('paprika-purge-chunks'), get_process_definition_id('paprika-purge-chunks-exceptions'));