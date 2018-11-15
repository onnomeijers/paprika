insert into process_definitions (name) values ('paprika-purge-messages');
insert into process_definitions (name) values ('paprika-purge-messages-exceptions');

insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-messages'), 'state.processing');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-messages'), 'purge.messages');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-messages'), 'state.processed');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-messages-exceptions'), 'state.failed');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages','state.processing'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages','state.processing'), 'state', 'PROCESSING');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages','purge.messages'), 'action', 'paprika.actions.events.PurgeMessages.PurgeMessages');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages','purge.messages'), 'days', '60');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages','state.processed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages','state.processed'), 'state', 'PROCESSED');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages-exceptions','state.failed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-messages-exceptions','state.failed'), 'state', 'FAILED');

insert into scheduled_events(name, repetition, expected, active, pdn_id, e_pdn_id) values ('paprika-purge-messages', 'DAYS', STR_TO_DATE('10-10-2016 23:00:00','%m-%d-%Y %H:%i:%s'), 1, get_process_definition_id('paprika-purge-messages'), get_process_definition_id('paprika-purge-messages-exceptions'));