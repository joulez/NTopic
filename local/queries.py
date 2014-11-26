QGetUserID = """
SELECT id FROM users WHERE value = ?;
"""

QSetUser = """
INSERT INTO users (value) VALUES (?);
"""

QGetChannelID = """
SELECT id FROM channels WHERE value = ?;
"""

QSetChannel = """
INSERT INTO channels (value, user_id) VALUES (?, ?);
"""

QGetTopicID = """
SELECT id FROM topic_ids WHERE value = ?;
"""

QSetTopic = """
INSERT INTO topic_ids (value, user_id, current_topic_id) VALUES (?, ?, ?);
"""

QGetTopicListID = """
SELECT id FROM topic_list WHERE value = ?;
"""

QSetTopicList = """
INSERT INTO topic_list (value, user_id) VALUES (?, ?);
"""

QGetTopicIDLogID = """
SELECT id FROM topic_id_logs WHERE topic_id_id = ? AND topic_log_id = ? AND
user_id = ?;

"""

QSetTopicIDLog = """
INSERT INTO topic_id_logs (topic_id_id, topic_log_id, user_id) VALUES (?, ?, ?);
"""

QGetTopicChannelID = """
SELECT id FROM topic_channels WHERE topic_id = ? AND channel_id = ?;
"""

QSetTopicChannel = """
INSERT INTO topic_channels (topic_id, channel_id) VALUES (?, ?);
"""

#DELETERS
QDelChannelTopic = """
DELETE FROM topic_channels WHERE topic_id = ? AND channel_id = ?;
"""

QCheckDB = """
SELECT last_access FROM config LIMIT 1;
"""

QUpdateDB = """
UPDATE config SET last_access = CURRENT_TIMESTAMP;
"""

QSchema = ["""
PRAGMA foreign_keys = OFF;
""","""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value TEXT UNIQUE NOT NULL
);
""","""
CREATE INDEX users_idx ON users(value);
""","""
CREATE TABLE topic_ids (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users,
    current_topic_id INTEGER NOT NULL REFERENCES topic_list DEFERRABLE INITIALLY DEFERRED
    );
""","""
CREATE INDEX topic_ids_user_idx ON topic_ids(user_id);
""","""
CREATE TABLE channels (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users
    );
""","""
CREATE INDEX channels_user_idx ON channels(user_id);
""","""
CREATE TABLE topic_list (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    value TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users
    );
""","""
CREATE INDEX topics_user_idx ON topic_list(user_id);
""","""
CREATE TABLE topic_id_logs (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    topic_id_id INTEGER NOT NULL REFERENCES topic_ids,
    topic_log_id INTEGER NOT NULL REFERENCES topic_list,
    user_id INTEGER NOT NULL REFERENCES users,
    UNIQUE (topic_id_id, topic_log_id, user_id)
    );
""","""
CREATE INDEX topic_id_logs_topic_log_idx ON topic_id_logs(topic_log_id);
""","""
CREATE INDEX topic_id_logs_topic_id_idx ON topic_id_logs(topic_id_id);
""","""
CREATE INDEX topic_id_logs_user_idx ON topic_id_logs(user_id);
""","""
CREATE TABLE topic_channels (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    topic_id INTEGER NOT NULL REFERENCES topic_ids,
    channel_id INTEGER NOT NULL REFERENCES channels
    );
""","""
CREATE INDEX topic_channels_topic_idx ON topic_channels(topic_id);
""","""
CREATE INDEX topic_channels_channel_idx ON topic_channels(channel_id);
""","""
CREATE TABLE cache (
    ts TEXT NOT NULL,
    channel TEXT NOT NULL,
    topic_group TEXT NOT NULL,
    topic TEXT NOT NULL
    );
""","""
CREATE TABLE config (
    last_access TEXT PRIMARY KEY,
    channel_count INT NOT NULL,
    group_count INT NOT NULL,
    topic_count INT NOT NULL
    ) WITHOUT ROWID;
""","""
INSERT INTO config VALUES (datetime('NOW'), 0, 0, 0);
""","""
PRAGMA foreign_keys = ON;
"""]

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
