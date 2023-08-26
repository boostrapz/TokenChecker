This is simple scanner for any TokenID ownership by Contract address.

To start you need install some Python libraries by this command in the directory of the program

pip install -r requirements.txt

Get API keys for needed scanners, you need to sign up account and go to "My API" settings and create one.

https://bscscan.com/myapikey
https://polygonscan.com/myapikey
https://etherscan.io/myapikey

Than save API key for each scan in respective file, for bscscan save your API key into bsc_api.txt , etc.

Insert the wallet addresses you need to check in wallets.txt

Run the program by calling in cmd prompt: python lovecheck.py