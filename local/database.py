from queries import *

def DBAddTopic(conn, user, channel, topicID, topic):
    userID = getSetValue(conn, (QGetUserID, (user,)), (QSetUser, (user,)))[1][0]
    channelID = getSetValue(conn, (QGetChannelID, (channel,)), (QSetChannel,
            (channel, userID)))[1][0]
    topicLogID = getSetValue(conn, (QGetTopicLogID, (topic,)),
            (QSetTopicLog, (topic, userID)))[1][0]
    topicID = getSetValue(conn, (QGetTopicID, (topicID,)), (QSetTopic,
            (topicID, userID, topicLogID)))[1][0]
    topicIDLogID = getSetValue(conn, (QGetTopicIDLogID, (topicID, topicLogID,
        userID)), (QSetTopicIDLog, (topicID, topicLogID, userID)))[1][0]
    topicChannelID = getSetValue(conn, (QGetTopicChannelID, (topicIDLogID,
        channelID)), (QSetTopicChannel, (topicIDLogID, channelID)))

    if topicChannelID[0] == True:
        return (False, topicChannelID[1][0], 'EXISTS')
    return (True, topicChannelID[1][0], None)

def getSetValue(conn, getQuery, setQuery, exists=True):
    """Getter/Setter function. Attempts to avoid concurrency issues. 
    lastrowid not supported. (might not be what is requested)
    """
    cursor = conn.cursor()
    try:
       cursor.execute(*getQuery)
       value = cursor.fetchone()
       if value:
           return (exists, value)
       raise ValueError('getSetValue(): getQuery returned None.')
    except:
        print('test')
        try:
            cursor.execute(*setQuery)
            conn.commit()
        except:
            return getSetValue(conn, getQuery, setQuery, False)
    return getSetValue(conn, getQuery, setQuery, False)

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
