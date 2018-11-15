CREATE INDEX mse_state_idx ON messages (state);
CREATE INDEX mse_hashcode_idx ON messages (hashcode);
CREATE INDEX mse_consumer_idx ON messages (consumer);
CREATE INDEX mse_consumer_state_idx ON messages (consumer, state);
CREATE INDEX mse_delay_state_idx ON messages (delay, state);