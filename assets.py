
ecu = {
    "7B0": 'ECU_ADDR_S',   # Skid Control address ECU
    "7B8": 'ECU_R_ADDR_S',  # Responses sent by 7B0 Skid Control ECU 7B0/7B8
    "7E2": 'ECU_ADDR_H',   # HVECU address (Hybrid contol module)
    "7EA": 'ECU_R_ADDR_H',  # Resp. sent by HVECU (Hybrid Ctrl module) 7E2/7EA
    "7E0": 'ECU_ADDR_E',   # Engine ECU address
    "7E8": 'ECU_R_ADDR_E',  # Responses sent by ECM (engine Ctrl module) 7E0/7E8
    "7E1": 'ECU_ADDR_T',   # Transmission ECU address
    "7E9": 'ECU_R_ADDR_T',  # Resp.sent by TCM (transmission Ctrl module)7E1/7E9
    "7C0": 'ECU_ADDR_I',   # ICE ECU address
    "7C8": 'ECU_R_ADDR_I',  # Responses sent by ICE ECU address 7C0/7C8
    "7E3": 'ECU_ADDR_B',   # Traction Battery ECU address
    "7EB": 'ECU_R_ADDR_B',  # Responses sent by Traction Battery ECU - 7E3/7EB
    "7C4": 'ECU_ADDR_P',   # Air Conditioning
    "7CC": 'ECU_R_ADDR_P'  # Responses sent by Air Conditioning ECU - 7C4/7CC
}

blacklisted_pids = (
    'CLEAR_DTC',  # Clear DTCs and Freeze data
    'ELM_DPN',  # 'Current protocol by number' ('AT DPN')
    'CUSTOM_SFS5',  # "Set Battery Cooling Fan Speed 5|A|0|0|No reply req'd" ('30810605')
    'CUSTOM_SFS2',  # "Set Battery Cooling Fan Speed 2|A|0|0|No reply req'd" ('30810602')
    'CUSTOM_SFS3',  # "Set Battery Cooling Fan Speed 3|A|0|0|No reply req'd" ('30810603')
    'CUSTOM_SFS0',  # "Set Battery Cooling Fan Speed 0 (Off)|A|0|0|No reply req'd" ('30810600')
    'CUSTOM_TRAC_DIS',  # "Disable Traction Control|A|0|0|No reply req'd" ('30610040')
    'CUSTOM_SFS4',  # "Set Battery Cooling Fan Speed 4|A|0|0|No reply req'd" ('30810604')
    'CUSTOM_SFS6',  # "Set Battery Cooling Fan Speed 6 (max.)|A|0|0|No reply req'd" ('30810606')
    'CUSTOM_SFS1',  # "Set Battery Cooling Fan Speed 1|A|0|0|No reply req'd" ('30810601')
    'CUSTOM_SBB_ENA_P',  # "Seat Belt Beep Enable Passenger Only|A|0|0|No reply req'd" ('3BA740')
    'CUSTOM_RB_ENA',  # "Reverse Beep Enable|A|0|0|No reply req'd" ('3BAC00')
    'CUSTOM_SBB_DIS_R',  # "Seat Belt Beep Disable Rear Only|A|0|0|No reply req'd" ('3BA7C0')
    'CUSTOM_SBB_DIS_D',  # "Seat Belt Beep Disable Driver Only|A|0|0|No reply req'd" ('3BA760')
    'CUSTOM_SBB_DIS_A',  # "Seat Belt Beep Disable All|A|0|0|No reply req'd" ('3BA700')
    'CUSTOM_SBB_DIS_P',  # "Seat Belt Beep Disable Passenger Only|A|0|0|No reply req'd" ('3BA7A0')
    'CUSTOM_SBB_ENA_D',  # "Seat Belt Beep Enable Driver Only|A|0|0|No reply req'd" ('3BA780')
    'CUSTOM_SBB_ENA_R',  # "Seat Belt Beep Enable Rear Only|A|0|0|No reply req'd" ('3BA720')
    'CUSTOM_SBB_ENA_A',  # "Seat Belt Beep Enable All|A|0|0|No reply req'd" ('3BA7E0')
    'CUSTOM_RB_DIS',  # "Reverse Beep Disable|A|0|0|No reply req'd" ('3BAC40')
)
