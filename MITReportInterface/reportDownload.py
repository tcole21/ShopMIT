import datetime
import requests
import hmac, hashlib
import base64
import xmltodict

access_Key = "9e92a9a2-ed6a-49f8-8d39-83e9d00434ec"
shared_Key = "H2nrnNNc9/SrjG+SXZ2RVylUUuQwfAzkDzcIyoM1gd8="
merchant_Id = "mit_test"
request_host = "apitest.cybersource.com"


def process_get():
        resource = "/reporting/v3/report-downloads?organizationId=mit_test&reportDate=2024-07-17&reportName=TDR_MIT"
        #resource = '/reporting/v3/reports?startTime=2024-01-01T00:00:00.0Z&endTime=2024-01-02T23:59:59.0Z&timeQueryType=executedTime&reportMimeType=application/xml'
        method = 'get'

        time = getCurrentDateTime()

        token = get_signature(method, resource, time)
        print(token)

        header_params = {}
        header_params['Accept'] = 'application/hal+json;charset=utf-8'
        header_params['Content-Type'] = 'application/json;charset=utf-8'
        header_params['Accept-Encoding'] = '*'
        header_params['v-c-merchant-id'] = merchant_Id
        header_params["Date"] = time
        header_params["Host"] = request_host
        #header_params["User-Agent"] = "Mozilla/5.0"

        header_params["Signature"] = token

        url = "https://" + request_host + resource

        print("\n -- RequestURL -- ")
        print("\tURL : " + url)
        print("\n -- HTTP Headers -- ")
        print("\tContent-Type : " + header_params['Content-Type'])
        print("\tv-c-merchant-id : " + header_params['v-c-merchant-id'])
        print("\tDate : " + header_params["Date"])
        print("\tHost : " + header_params["Host"])
        print("\tSignature : " + header_params["Signature"])

        response = requests.get(url, headers=header_params)
        status = response.status_code
        print(status)
        reportDict = xmltodict.parse(response.content)

        return status, reportDict

        

def getCurrentDateTime():
    now = datetime.datetime.now(datetime.timezone.utc) 
    Date = now.strftime("%a, %d %b %Y %X")
    #print(Date + ' GMT')
    return Date + " GMT"



def get_signature(method, resource, time):
        # Getting HTTP Signature
        header_list = ([])

        # Key id is the key obtained from EBC
        header_list.append("keyid=\"" + str(access_Key) + "\"")
        header_list.append(", algorithm=\"HmacSHA256\"")

       
        getheaders = "host date request-target v-c-merchant-id"
        header_list.append(", headers=\"" + getheaders + "\"")

        signature_list = ([])

        # This method adds the host header
        signature_list.append("host: " + request_host + "\n")

        # This method adds the date header
        signature_list.append("date: " + time + "\n")

        # This method adds the request target
        signature_list.append("request-target: ")

        request_target = method + " " + resource
        signature_list.append(request_target + "\n")


        # This method adds the v-c-merchant-id header
        signature_list.append("v-c-merchant-id: " + merchant_Id)

        sig_value = "".join(signature_list)

        sig_value_string = str(sig_value)
        sig_value_utf = bytes(sig_value_string, encoding='utf-8')

        secret = base64.b64decode(shared_Key)

        hash_value = hmac.new(secret, sig_value_utf, hashlib.sha256)

        signature = base64.b64encode(hash_value.digest()).decode("utf-8")

        header_list.append(", signature=\"" + signature + "\"")
        token = ''.join(header_list)

        return token



