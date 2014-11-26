from queries import *
from exceptions import *
import sqlite3

def DBAddChannelTopic(conn, user, channel, topicID, topic):
    userID = getSetValue(conn, (QGetUserID, (user,)), (QSetUser, (user,)))[1][0]
    channelID = getSetValue(conn, (QGetChannelID, (channel,)), (QSetChannel,
            (channel, userID)))[1][0]
    topicLogID = getSetValue(conn, (QGetTopicListID, (topic,)),
            (QSetTopicList, (topic, userID)))[1][0]
    topicIDID = getSetValue(conn, (QGetTopicID, (topicID,)), (QSetTopic,
            (topicID, userID, topicLogID)))[1][0]
    topicIDLogID = getSetValue(conn, (QGetTopicIDLogID, (topicIDID, topicLogID,
        userID)), (QSetTopicIDLog, (topicIDID, topicLogID, userID)))[1][0]
    topicChannelID = getSetValue(conn, (QGetTopicChannelID, (topicIDID,
        channelID)), (QSetTopicChannel, (topicIDID, channelID)))

    if topicChannelID[0] == True:
        return (False, topicChannelID[1][0], 'EXISTS')
    return (True, topicChannelID[1][0], None)

def DBRemoveChannelTopic(conn, user, channel, topicID):
    userID = getSetValue(conn, (QGetUserID, (user,)), (QSetUser, (user,)))[1][0]
    channelID = getValue(conn, (QGetChannelID, (channel,)))
    if not channelID:
        raise ValueError(format('No topics registered with channel \"%s\"',
            channel))
    channelID = channelID[0]
    topicIDID = getValue(conn, (QGetTopicID, (topicID,)))
    if not topicIDID:
        raise ValueError(format('Topic ID \"%s\" doesn\'t exist.', topicID))
    topicIDID = topicIDID[0]
    setValue(conn, (QDelChannelTopic, (topicIDID, channelID)))

def getSetValue(conn, getQuery, setQuery, exists=True):
    """Getter/Setter function. Attempts to avoid concurrency issues. 
    lastrowid not supported. (might not be what is requested)
    """
    cursor = conn.cursor()
    try:
       value = getValue(conn, getQuery)
       if value:
           return (exists, value)
       raise ValueError('getSetValue(): getValue() returned None.')
    except:
        print('test')
        try:
            setValue(conn, setQuery)
        except sqlite3.IntegrityError:
            return getSetValue(conn, getQuery, setQuery, False)
        except sqlite3.Error as e:
            raise DBError(e.args[0])
    return getSetValue(conn, getQuery, setQuery, False)

def getValue(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(*query)
        return cursor.fetchone()
    except Exception as e:
        raise DBError(e.value)

def setValue(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(*query)
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.rollback()

#Testing function leave at the bottom to avoid diff mangling.
def _getSetValue(conn, getQuery, setQuery, exists=True):
    """Getter/Setter function. Attempts to avoid concurrency issues. 
    lastrowid not supported. (might not be what is requested)
    """
    cursor = conn.cursor()
    if True:
        cursor.execute(*getQuery)
        value = cursor.fetchone()
        if value:
            return (exists, value)
        raise ValueError('getSetValue(): getQuery returned None.')
    else:
        try:
            cursor.execute(*setQuery)
            conn.commit()
        except:
            return getSetValue(conn, getQuery, setQuery, False)
    return getSetValue(conn, getQuery, setQuery, True)

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
