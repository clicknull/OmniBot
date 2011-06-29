import OmniLib
import OmniLib.debug
import OmniLib.Auth.smtp
import OmniLib.Auth.pastebin

authd_users = {}
trustd_users = []

def init():
    OmniLib.debug.debug("Initializing Authentication module")

    #ahem some default test options anyone?
    OmniLib.Auth.irc_auth.trustd_users.append(":pasv!~l@sa-9AC43B12.socal.res.rr.com")
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"] = {} # inside the dictionary is another dictionary :)
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"]["priv_level"] = "admin" # privlevels admin - user
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"]["timeleft"] = 9999999 # when timeleft =< 0 authflag sets to false
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"]["email"] = "pasvninja@gmail.com" # email to send genkey to
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"]["authflag"] = True # determines if the user is genkeyed or not
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"]["genkey"] = "z85qZo!skdq"
    OmniLib.Auth.irc_auth.authd_users[":pasv!~l@sa-9AC43B12.socal.res.rr.com"]["private_key"] = "priv8"

def keygen(userstring, private_key):
    if(userstring not in trustd_users):
	# log attempt!
	return -1
    # insert keygenning code here. 
    msg = "User: " + userstring + " has generated this key: " + genkey
    if(authd_users[userstring]['email'] == "pastebin"):
	url=OmniLib.Auth.pastebin.post_it(msg) #yes that is insecure but some people dont have gmail..
	return url
    else:
	OmniLib.Auth.smtp.send_email(authd_users[userstring]['email'], msg)
	return 0

def auth_request(userstring, private_key, genkey):
    if(not authd_users.has_key(userstring)):
	return -1
    if(authd_users[userstring]['private_key'] != private_key or authd_users[userstring]['genkey'] != genkey):
	return -1
    else:
	authd_users[userstring]['authflag'] = True
	authd_users[userstring]['timeout'] = 60*60 # redundant?
	return 1 # success

# we should really hash/encrypt the genkey/authkey with DES or something..
def add_trusted(userstring, priv_level, email):
    if(not authd_users.has_key(userstring)):
	authd_users[userstring] = {}
	authd_users[userstring]['priv_level'] = priv_level
	authd_users[userstring]['timeleft'] = 60*60 # (in seconds) 1 hour; kind of harsh?
	authd_users[userstring]['email'] = email
	authd_users[userstring]['authflag'] = False # default: every user starts out unauth'd
	authd_users[userstring]['private_key'] = "changeme" # find a better way to do this
	authd_users[userstring]['genkey'] = "" # check against this later #add timeout to this as well..
    else:
	return -1 # user exists! use mod_users()
	
def del_trusted(userstring): #note this is for the trusted list not the authd_users
    if(userstring in trustd_users):
	del trustd_users[userstring]
	#del authd_users[userstring]
    else:
	return -1
