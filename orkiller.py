import praw, time, datetime, traceback, obot, re
#obot is used to login with OAuth, you will get an exception if you attempt to import it

"""
Remove and tempban script users.
"""

#login using file with oauth app details
r = obot.login()

#create empty arrays so we don't act on things twice
recentlyDonePosts = []
recentlyBannedUsers = []
recentlyModdedSubs = []

testMode = False
botActive = True

#get posts from /r/mod
rmod = r.get_subreddit("mod")


#string sent to user
sentToUserString = "You have been temporarily banned for using a comment overwrite script. This is considered spam. In future, please use a less spammy overwrite message. Thank you."

def isSpam(string):
        notanum = 0
        caps = 0
        spaces = 0
        instring = string
        for x in instring:
            if bool(re.search("([^A-Za-z0-9 ])", x)):
                notanum += 1
            if bool(re.search("([A-Z])", x)):
                caps += 1
            if x == " ":
                spaces += 1
        if len(string) <20 and len(string) != 1:
            return False
        percent = (notanum / len(instring))*100
        capsPercent = (caps / len(instring))*100
        if percent >=20 and spaces/len(string) < 0.05 and len:
            if "[](" in string:
                return False
            else:
                if capsPercent > 30 and capsPercent < 50:
                    return True
                else:
                    return False 
        return False


def is_banned(sub, user):
    if [i for i in list(r.get_banned(sub)) if i.name == user]:
        return True
    return False

#post checker method
def check():
        stream = rmod.get_edited(limit=100)
        #this phrase is always found in the comments
        scriptKeyword = "This comment has been overwritten by"
        #make sure we get the right thing
        for comment in stream:
            try:
                text = comment.body
            except AttributeError:
                text = comment.selftext
            #set up some bools
            overwriteMessageInText = scriptKeyword in text
            itemNotDone = comment.id not in recentlyDonePosts
            itemIsGibberish = isSpam(text)
            either = overwriteMessageInText or itemIsGibberish
            
            if either and itemNotDone:
                if comment.banned_by == None:
                        #string for mod note
                        subofcomment = comment.subreddit
                        modString = "Greasemonkey overwrite script:", comment.id
                        
                        #don't try to ban deleted users
                        if comment.author == None:
                            cmtAuthor = "[deleted]"
                        else:
                            cmtAuthor = comment.author.name
                        
                        #ban args
                        banargs = {"duration": 3, "note": modString, "ban_message": sentToUserString}
                        
                        #send item to spam filter if it's gibberish
                        if(itemIsGibberish):
                            if not testMode:
                                comment.remove(spam=True)
                            print("Removed id " + comment.id + " by " + cmtAuthor + " from /r/" + comment.subreddit.display_name + ". (gibberish comment)")
                            print("        Text:", text)
                        else:
                            if not testMode:
                                comment.remove(spam=False)
                            print("Removed id " + comment.id + " by " + cmtAuthor + " from /r/" + comment.subreddit.display_name)
                            print("        Text:", text)
                        if not testMode:
                            recentlyDonePosts.append(comment.id)
                        
                        #don't bother banning them if they're already banned
                        try:
                            if is_banned(subofcomment, cmtAuthor) or cmtAuthor in recentlyBannedUsers:
                                pass
                            else:
                                if cmtAuthor == "[deleted]":
                                    pass
                                else:
                                    if not testMode:
                                        rmod.add_ban(subofcomment, **banargs)
                                        recentlyBannedUsers.append(cmtAuthor)
                                    print("Tempbanned " + cmtAuthor + " in " + "/r/" + comment.subreddit.display_name)
                        except:
                            recentlyBannedUsers.append(cmtAuthor)
                            print("Couldn't ban " + cmtAuthor + " from /r/" + comment.subreddit.display_name + ". No access permission?")
                        
                        
                        
        #let's relax a little
        time.sleep(1)
def getTime():
    return round(time.time()*1000)
    
if testMode:
    print("/!\ TEST MODE! All actions are SIMULATED.")
while True:
    try:
        check()
    except Exception as e:
        fileName = str(getTime()) + ".txt"
        print("exception occurred! sleeping 10 seconds. written to file")
        exFile = open(fileName, 'w')
        exFile.write(str(e))
        exFile.close()
        time.sleep(10)
        
