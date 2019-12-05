import json
import random
import array as arr

timeLimit2PING = 60
timeLimit2SendPING = 1.5
offlineTimeout = 5
timeLimitAcceptJoin = 30

# define the special symbol in Lora messages 
HUB_LORA_ID                   = '0000'
HUB_lora_chanel               = '19'
endMessSymbol                 = 'AB'
joinNetworkHeader             = 'A0A1A2'
join_lora_network_ACK         = 'A2A2A2'
join_lora_network_accepted    = 'A2A1A0'
sendUpdateHeader              = 'B0B1B0'
UpdateDataHeader_ACK          = 'B2B2B2'
requestToUpdateDataHeader     = 'B2B1B0'
actionToNodeHeader            = 'B9B8B9'
PINGMessHeader                = 'B4B3B4B0'
pingToHub                     = 'B3B4B3B0'
ADDR_HW                       = '50'
ADDR_LW                       = '50'
# mark
markMess_SensorNode           = 'D1D3D1'

# convert from string to bytes
Str_HUB_LORA_ID                = (bytes.fromhex(HUB_LORA_ID)).decode(encoding = 'cp855', errors='strict')
Str_HUB_lora_chanel            = (bytes.fromhex(HUB_lora_chanel)).decode(encoding = 'cp855', errors='strict')
Str_endMessSymbol              = (bytes.fromhex(endMessSymbol)).decode(encoding = 'cp855', errors='strict')
Str_joinNetworkHeader          = (bytes.fromhex(joinNetworkHeader)).decode(encoding = 'cp855', errors='strict')
Str_join_lora_network_ACK      = (bytes.fromhex(join_lora_network_ACK)).decode(encoding = 'cp855', errors='strict')
Str_join_lora_network_accepted = (bytes.fromhex(join_lora_network_accepted)).decode(encoding = 'cp855', errors='strict')
Str_sendUpdateHeader           = (bytes.fromhex(sendUpdateHeader)).decode(encoding = 'cp855', errors='strict')
Str_UpdateDataHeader_ACK       = (bytes.fromhex(UpdateDataHeader_ACK)).decode(encoding = 'cp855', errors='strict')
Str_requestToUpdateDataHeader  = (bytes.fromhex(requestToUpdateDataHeader)).decode(encoding = 'cp855', errors='strict')
Str_actionToNodeHeader         = (bytes.fromhex(actionToNodeHeader)).decode(encoding = 'cp855', errors='strict')
Str_PINGMessHeader             = (bytes.fromhex(PINGMessHeader)).decode(encoding = 'cp855', errors='strict')
Str_pingToHub                  = (bytes.fromhex(pingToHub)).decode(encoding = 'cp855', errors='strict')
Str_markMess_SensorNode        = (bytes.fromhex(markMess_SensorNode)).decode(encoding = 'cp855', errors='strict')
Str_ADDR_HW                    = (bytes.fromhex(ADDR_HW)).decode(encoding = 'cp855', errors='strict')
Str_ADDR_LW                   = (bytes.fromhex(ADDR_LW)).decode(encoding = 'cp855', errors='strict')

# global varible

StrStatus1 = "Off Line" 
StrStatus2 = "On Line" 

Data = arr.array('i',[0, 0, 0, 0, 0, 0]) 
Data2 = arr.array('i',[0, 0, 0, 0, 0, 0]) 
DataCheckIn = arr.array('i',[0, 0]) 
PositionAccess = False
PositionNum = 0
FingerData = ["","",""]
ACKDevice1 = "A:FG2301"
ACKDevice2 = "A:FG2302"

KEYID_HUB = "FG1234"

receive_WARMessage = False
