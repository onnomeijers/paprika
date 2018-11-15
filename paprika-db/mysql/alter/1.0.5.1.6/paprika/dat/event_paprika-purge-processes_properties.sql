insert into process_definitions (name) values ('paprika-purge-processes_properties');
insert into process_definitions (name) values ('paprika-purge-processes_properties-exceptions');

insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-processes_properties'), 'state.processing');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-processes_properties'), 'purge.processes_properties');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-processes_properties'), 'state.processed');
insert into process_definitions_actions (pdn_id, name) values (get_process_definition_id('paprika-purge-processes_properties-exceptions'), 'state.failed');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties','state.processing'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties','state.processing'), 'state', 'PROCESSING');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties','purge.processes_properties'), 'action', 'paprika.actions.events.PurgeProcessesProperties.PurgeProcessesProperties');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties','purge.processes_properties'), 'days', '60');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties','state.processed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties','state.processed'), 'state', 'PROCESSED');

insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties-exceptions','state.failed'), 'action', 'paprika.actions.events.State.State');
insert into process_definitions_actions_properties (dan_id, name, value) values (get_process_definition_action_id('paprika-purge-processes_properties-exceptions','state.failed'), 'state', 'FAILED');

insert into scheduled_events(name, repetition, expected, active, pdn_id, e_pdn_id) values ('paprika-purge-processes_properties', 'DAYS', STR_TO_DATE('10-10-2016 23:00:00','%m-%d-%Y %H:%i:%s'), 1, get_process_definition_id('paprika-purge-processes_properties'), get_process_definition_id('paprika-purge-processes_properties-exceptions'));