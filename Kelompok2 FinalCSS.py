from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np

app = Flask(__name__)
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        creditLimit = request.form.get('creditLimit')
        availableMoney = request.form.get('availableMoney')
        transactionAmount = request.form.get('transactionAmount')
        currentBalance = request.form.get('currentBalance')
        cardPresent = request.form.get('cardPresent')
        expirationDateKeyInMatch = request.form.get('expirationDateKeyInMatch')
        transactionHour = request.form.get('transactionHour')
        transactionDayOfWeek = request.form.get('transactionDayOfWeek')
        transactionDay = request.form.get('transactionDay')
        transactionMonth = request.form.get('transactionMonth')
        CVVMatch = request.form.get('CVVMatch')
        weekend = request.form.get('weekend')
        workHour = request.form.get('workHour')
        AfterPaymentSalary = request.form.get('AfterPaymentSalary')
        diff_weeks = request.form.get('diff_weeks')
        daysSinceRegister = request.form.get('daysSinceRegister')
        daysToExpiration = request.form.get('daysToExpiration')
        daySinceLastAddressChange = request.form.get('daySinceLastAddressChange')
        LastAddressChangeDiff = request.form.get('LastAddressChangeDiff')
        acqCountry = request.form.get('acqCountry')
        posConditionCode = request.form.get('posConditionCode')
        posEntryMode = request.form.get('posEntryMode')
        transactionType = request.form.get('transactionType')
        merchantCategoryCode = request.form.get('merchantCategoryCode')
        merchantCountryCode = request.form.get('merchantCountryCode')
        categoryTransaction = request.form.get('categoryTransaction')
        
        if acqCountry == 'CAN':
            ValacqCountryCAN = 1
            ValacqCountryMEX = 0
            ValacqCountryPR = 0
            ValacqCountryUS = 0
            ValacqCountryUnknown = 0
        elif acqCountry == 'MEX':
            ValacqCountryCAN = 0
            ValacqCountryMEX = 1
            ValacqCountryPR = 0
            ValacqCountryUS = 0
            ValacqCountryUnknown = 0     
        elif acqCountry == 'PR':
            ValacqCountryCAN = 0
            ValacqCountryMEX = 0
            ValacqCountryPR = 1
            ValacqCountryUS = 0
            ValacqCountryUnknown = 0
        elif acqCountry == 'US':
            ValacqCountryCAN = 0
            ValacqCountryMEX = 0
            ValacqCountryPR = 0
            ValacqCountryUS = 1
            ValacqCountryUnknown = 0
        elif acqCountry == 'Unknown':
            ValacqCountryCAN = 0
            ValacqCountryMEX = 0
            ValacqCountryPR = 0
            ValacqCountryUS = 0
            ValacqCountryUnknown = 1

        if posConditionCode == '1.0':
            ValposConditionCode1 = 1
            ValposConditionCode8 = 0
            ValposConditionCode99 = 0
            ValposConditionCodeUnknown = 0
        elif posConditionCode == '8.0':
            ValposConditionCode1 = 0
            ValposConditionCode8 = 1
            ValposConditionCode99 = 0
            ValposConditionCodeUnknown = 0
        elif posConditionCode == '99.0':
            ValposConditionCode1 = 0
            ValposConditionCode8 = 0
            ValposConditionCode99 = 1
            ValposConditionCodeUnknown = 0
        elif posConditionCode == 'Unknown':
            ValposConditionCode1 = 0
            ValposConditionCode8 = 0
            ValposConditionCode99 = 0
            ValposConditionCodeUnknown = 1
           
        if posEntryMode == '2.0':
            ValposEntryMode2 = 1
            ValposEntryMode5 = 0
            ValposEntryMode80 = 0
            ValposEntryMode9 = 0
            ValposEntryMode90 = 0            
            ValposEntryModeUnknown = 0
        elif posEntryMode == '5.0':
            ValposEntryMode2 = 0
            ValposEntryMode5 = 1
            ValposEntryMode80 = 0
            ValposEntryMode9 = 0
            ValposEntryMode90 = 0            
            ValposEntryModeUnknown = 0
        elif posEntryMode == '80.0':
            ValposEntryMode2 = 0
            ValposEntryMode5 = 0
            ValposEntryMode80 = 1
            ValposEntryMode9 = 0
            ValposEntryMode90 = 0            
            ValposEntryModeUnknown = 0
        elif posEntryMode == '9.0':
            ValposEntryMode2 = 0
            ValposEntryMode5 = 0
            ValposEntryMode80 = 0
            ValposEntryMode9 = 1
            ValposEntryMode90 = 0            
            ValposEntryModeUnknown = 0            
        elif posEntryMode == '90.0':
            ValposEntryMode2 = 0
            ValposEntryMode5 = 0
            ValposEntryMode80 = 0
            ValposEntryMode9 = 0
            ValposEntryMode90 = 1            
            ValposEntryModeUnknown = 0
        elif posEntryMode == 'Unknown':
            ValposEntryMode2 = 0
            ValposEntryMode5 = 0
            ValposEntryMode80 = 0
            ValposEntryMode9 = 0
            ValposEntryMode90 = 0            
            ValposEntryModeUnknown = 1

        if transactionType == 'ADDRESS_VERIFICATION':
            ValtransactionTypeAddVer = 1
            ValtransactionTypePurchase = 0
            ValtransactionTypeReversal = 0
            ValtransactionTypeUnknown = 0
        elif transactionType == 'PURCHASE':
            ValtransactionTypeAddVer = 0
            ValtransactionTypePurchase = 1
            ValtransactionTypeReversal = 0
            ValtransactionTypeUnknown = 0            
        if transactionType == 'REVERSAL':
            ValtransactionTypeAddVer = 0
            ValtransactionTypePurchase = 0
            ValtransactionTypeReversal = 1
            ValtransactionTypeUnknown = 0
        elif transactionType == 'Unknown':
            ValtransactionTypeAddVer = 0
            ValtransactionTypePurchase = 0
            ValtransactionTypeReversal = 0
            ValtransactionTypeUnknown = 1
            
        if merchantCategoryCode == 'airline':
            ValmerchantCategoryCodeAirline = 1
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'auto':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 1
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'cable or phone':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 1
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'entertainment':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 1
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'fastfood':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 1
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'food':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 1
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'food delivery':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 1
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'fuel':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 1
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'furniture':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 1
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'gym':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 1            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'health':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 1
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'hotels':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 1
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'mobile apps':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 1
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'online gifts':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 1
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'online retail':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 1
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'personal care':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 1
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'rideshare':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 1
            ValmerchantCategoryCodeSub = 0
        elif merchantCategoryCode == 'subscriptions':
            ValmerchantCategoryCodeAirline = 0
            ValmerchantCategoryCodeAuto = 0
            ValmerchantCategoryCodeCablePhone = 0
            ValmerchantCategoryCodeEntertaiment = 0
            ValmerchantCategoryCodeFastfood = 0
            ValmerchantCategoryCodeFood = 0
            ValmerchantCategoryCodeFoodDelivery = 0
            ValmerchantCategoryCodeFuel = 0
            ValmerchantCategoryCodeFurniture = 0
            ValmerchantCategoryCodeGym = 0            
            ValmerchantCategoryCodeHealth = 0
            ValmerchantCategoryCodeHotels = 0
            ValmerchantCategoryCodeMobileapps = 0
            ValmerchantCategoryCodeOnlineGifts = 0
            ValmerchantCategoryCodeOnlineRetail = 0
            ValmerchantCategoryCodeOnlineSub = 0
            ValmerchantCategoryCodePersonalCare = 0
            ValmerchantCategoryCodeRideshare = 0
            ValmerchantCategoryCodeSub = 1

        if merchantCountryCode == 'CAN':
            ValmerchantCountryCodeCAN = 1
            ValmerchantCountryCodeMEX = 0
            ValmerchantCountryCodePR = 0
            ValmerchantCountryCodeUS = 0
            ValmerchantCountryCodeUnknown = 0
        elif merchantCountryCode == 'MEX':
            ValmerchantCountryCodeCAN = 0
            ValmerchantCountryCodeMEX = 1
            ValmerchantCountryCodePR = 0
            ValmerchantCountryCodeUS = 0
            ValmerchantCountryCodeUnknown = 0
        elif merchantCountryCode == 'PR':
            ValmerchantCountryCodeCAN = 0
            ValmerchantCountryCodeMEX = 0
            ValmerchantCountryCodePR = 1
            ValmerchantCountryCodeUS = 0
            ValmerchantCountryCodeUnknown = 0
        elif merchantCountryCode == 'US':
            ValmerchantCountryCodeCAN = 0
            ValmerchantCountryCodeMEX = 0
            ValmerchantCountryCodePR = 0
            ValmerchantCountryCodeUS = 1
            ValmerchantCountryCodeUnknown = 0
        elif merchantCountryCode == 'Unknown':
            ValmerchantCountryCodeCAN = 0
            ValmerchantCountryCodeMEX = 0
            ValmerchantCountryCodePR = 0
            ValmerchantCountryCodeUS = 0
            ValmerchantCountryCodeUnknown = 1
            
        if categoryTransaction == 'High':
            ValcategoryTransactionHigh = 1
            ValcategoryTransactionMedium = 0
            ValcategoryTransactionLow = 0
        elif categoryTransaction == 'Medium':
            ValcategoryTransactionHigh = 0
            ValcategoryTransactionMedium = 1
            ValcategoryTransactionLow = 0
        elif categoryTransaction == 'Low':
            ValcategoryTransactionHigh = 0
            ValcategoryTransactionMedium = 0
            ValcategoryTransactionLow = 1
                        
        #datapredict = [creditLimit,
        datapredict = [[
                        creditLimit,                
                        availableMoney,
                        transactionAmount,
                        currentBalance,
                        cardPresent,
                        expirationDateKeyInMatch,
                        transactionHour,
                        transactionDayOfWeek,
                        transactionDay,
                        transactionMonth,
                        CVVMatch,
                        weekend,
                        workHour,
                        AfterPaymentSalary,
                        diff_weeks,
                        daysSinceRegister,
                        daysToExpiration,
                        daySinceLastAddressChange,
                        LastAddressChangeDiff,
                        ValacqCountryCAN,
                        ValacqCountryMEX,
                        ValacqCountryPR,
                        ValacqCountryUS,
                        ValacqCountryUnknown,
                        ValposConditionCode1,
                        ValposConditionCode8,
                        ValposConditionCode99,
                        ValposConditionCodeUnknown,
                        ValposEntryMode2,
                        ValposEntryMode5,
                        ValposEntryMode80,
                        ValposEntryMode9,
                        ValposEntryMode90,
                        ValposEntryModeUnknown,
                        ValtransactionTypeAddVer,
                        ValtransactionTypePurchase,
                        ValtransactionTypeReversal,
                        ValtransactionTypeUnknown,
                        ValmerchantCategoryCodeAirline,
                        ValmerchantCategoryCodeAuto,
                        ValmerchantCategoryCodeCablePhone,
                        ValmerchantCategoryCodeEntertaiment,
                        ValmerchantCategoryCodeFastfood,
                        ValmerchantCategoryCodeFood,
                        ValmerchantCategoryCodeFoodDelivery,
                        ValmerchantCategoryCodeFuel,
                        ValmerchantCategoryCodeFurniture,
                        ValmerchantCategoryCodeGym,
                        ValmerchantCategoryCodeHealth,
                        ValmerchantCategoryCodeHotels,
                        ValmerchantCategoryCodeMobileapps,
                        ValmerchantCategoryCodeOnlineGifts,
                        ValmerchantCategoryCodeOnlineRetail,
                        ValmerchantCategoryCodeOnlineSub,
                        ValmerchantCategoryCodePersonalCare,
                        ValmerchantCategoryCodeRideshare,
                        ValmerchantCategoryCodeSub,
                        ValmerchantCountryCodeCAN,
                        ValmerchantCountryCodeMEX,
                        ValmerchantCountryCodePR,
                        ValmerchantCountryCodeUS,
                        ValmerchantCountryCodeUnknown,
                        ValcategoryTransactionHigh,
                        ValcategoryTransactionLow,
                        ValcategoryTransactionMedium
                ]] 
##        columnspredict = ["creditLimit",
        columnspredict = [
                          "creditLimit",
                          "availableMoney",
                          "transactionAmount",
                          "currentBalance",
                          "cardPresent",
                          "expirationDateKeyInMatch",
                          "transactionHour",
                          "transactionDayOfWeek",
                          "transactionDay",
                          "transactionMonth",
                          "CVVMatch",
                          "weekend",
                          "workHour",
                          "AfterPaymentSalary",
                          "diff_weeks",
                          "daysSinceRegister",
                          "daysToExpiration",
                          "daySinceLastAddressChange",
                          "LastAddressChangeDiff",
                          "acqCountry_CAN",
                          "acqCountry_MEX",
                          "acqCountry_PR",
                          "acqCountry_US",
                          "acqCountry_Unkown",
                          "posConditionCode_1.0",
                          "posConditionCode_8.0",
                          "posConditionCode_99.0",
                          "posConditionCode_Unknown",
                          "posEntryMode_2.0",
                          "posEntryMode_5.0",
                          "posEntryMode_80.0",
                          "posEntryMode_9.0",
                          "posEntryMode_90.0",
                          "posEntryMode_Unknown",
                          "transactionType_ADDRESS_VERIFICATION",
                          "transactionType_PURCHASE",
                          "transactionType_REVERSAL",
                          "transactionType_Unknown",
                          "merchantCategoryCode_airline",
                          "merchantCategoryCode_auto",
                          "merchantCategoryCode_cable/phone",
                          "merchantCategoryCode_entertainment",
                          "merchantCategoryCode_fastfood",
                          "merchantCategoryCode_food",
                          "merchantCategoryCode_food_delivery",
                          "merchantCategoryCode_fuel",
                          "merchantCategoryCode_furniture",
                          "merchantCategoryCode_gym",
                          "merchantCategoryCode_health",
                          "merchantCategoryCode_hotels",
                          "merchantCategoryCode_mobileapps",
                          "merchantCategoryCode_online_gifts",
                          "merchantCategoryCode_online_retail",
                          "merchantCategoryCode_online_subscriptions",
                          "merchantCategoryCode_personal care",
                          "merchantCategoryCode_rideshare",
                          "merchantCategoryCode_subscriptions",
                          "merchantCountryCode_CAN",
                          "merchantCountryCode_MEX",
                          "merchantCountryCode_PR",
                          "merchantCountryCode_US",
                          "merchantCountryCode_Unknown",
                          "categoryTransaction_High",
                          "categoryTransaction_Low",
                          "categoryTransaction_Medium"
                ]

        print(datapredict)
        print(columnspredict)
        
        query = pd.DataFrame(data=datapredict, columns=columnspredict)                                  
        #query = pd.DataFrame(json)                                            
        query = query.reindex(columns=model_columns, fill_value = 0)
        #prediction = list(lr.predict(query))
        prediction =str(lr.predict(query))
        if prediction == '[0]':
            result = 'Non Fraud Transaction'
        elif prediction == '[1]':    
            result = 'Fraud Transaction'
        return '''<h1>The prediction value is: {}</h1>'''.format(str(result))
        #return data

    return '''<html>
                <head>
                        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
                        <title></title>                      
                </head>
                <body> 
                        <div class="container">
                                <form method="POST">
                                  <div class="form-row">
                                        <div class="form-group col-md-4">
                                          <h2>Fraud Detection Engine</h2>
                                        </div>
                                        <div class="form-group col-md-4">
                                        </div>
                                        <div class="form-group col-md-4">
                                        </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Credit Limit :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'creditLimit' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Available Money :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'availableMoney' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Transaction Amount :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'transactionAmount' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Current Balance :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'currentBalance' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Card Present :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'cardPresent' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Expiration Date Key In Match :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'expirationDateKeyInMatch' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Transaction Hour :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'transactionHour' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Transaction Day Of Week :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'transactionDayOfWeek' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>                                  
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Transaction Day :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'transactionDay' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Transaction Month :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'transactionMonth' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">CVV Match :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'CVVMatch' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Weekend :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'weekend' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Work Hour :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'workHour' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">After Payment Salary :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'AfterPaymentSalary' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Diff Weeks :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'diff_weeks' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Days Since Register :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'daysSinceRegister' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Days To Expiration :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'daysToExpiration' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Day Since Last Address Change :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'daySinceLastAddressChange' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="inputEmail4">Last Address Change Diff :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <input class="form-control" name = 'LastAddressChangeDiff' required="required">
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Acq Country">Choose Acq Country :</label><br>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="acqCountry" id="acqCountry">
                                        <option value="CAN">CAN</option>
                                        <option value="MEX">MEX</option>
                                        <option value="PR">PR</option>
                                        <option value="US">US</option>
                                        <option value="Unknown">Unknown</option>
                                      </select>
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Fos Condition Code:">Pos Condition Code :</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="posConditionCode" id="posConditionCode">
                                        <option value="1.0">1.0</option>
                                        <option value="8.0">8.0</option>
                                        <option value="99.0">99.0</option>
                                        <option value="Unknown">Unknown</option>
                                      </select>  
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>                                  
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Pos Entry Mode:">Choose Pos Entry Mode:</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="posEntryMode" id="posEntryMode">
                                        <option value="2.0">2.0</option>
                                        <option value="5.0">5.0</option>
                                        <option value="80.0">80.0</option>
                                        <option value="9.0">9.0</option>
                                        <option value="90.0">90.0</option>
                                        <option value="Unknown">Unknown</option>
                                      </select>                                    
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Transaction Type:">Choose Transaction Type:</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="transactionType" id="transactionType">
                                        <option value="ADDRESS_VERIFICATION">Address verification</option>
                                        <option value="PURCHASE">Purchase</option>
                                        <option value="REVERSAL">Reversal</option>
                                        <option value="Unknown">Unknown</option>
                                      </select>                                    
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>                                  
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Merchant Category Code:">Merchant Category Code:</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="merchantCategoryCode" id="merchantCategoryCode">
                                        <option value="airline">Airline</option>
                                        <option value="auto">Auto</option>
                                        <option value="Cable or Phone">cable/phone</option>
                                        <option value="Entertainment">entertainment</option>
                                        <option value="Fastfood">fastfood</option>
                                        <option value="Food">food</option>
                                        <option value="Food Delivery">food delivery</option>
                                        <option value="fuel">Fuel</option>
                                        <option value="furniture">Furniture</option>
                                        <option value="gym">Gym</option>
                                        <option value="health">Health</option>
                                        <option value="hotels">Hotels</option>
                                        <option value="mobile apps">Mobile Apps</option>
                                        <option value="online gifts">Online Gifts</option>
                                        <option value="online retail">Online Retail</option>
                                        <option value="online subscriptions">Online Subscriptions</option>
                                        <option value="personal care">Personal Care</option>
                                        <option value="rideshare">Rideshare</option>
                                        <option value="subscriptions">Subscriptions</option>
                                      </select>                                   
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Merchant Country Code">Choose Merchant Country Code:</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="merchantCountryCode" id="merchantCountryCode">
                                        <option value="CAN">CAN</option>
                                        <option value="MEX">MEX</option>
                                        <option value="PR">PR</option>
                                        <option value="US">US</option>
                                        <option value="Unknown">Unknown</option>
                                      </select>                                    
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>
                                  <div class="form-row">
                                    <div class="form-group col-md-4">
                                      <label for="Category Transaction">Choose Category Transaction:</label>
                                    </div>
                                    <div class="form-group col-md-4">
                                      <select name="categoryTransaction" id="categoryTransaction">
                                        <option value="High">High</option>
                                        <option value="Medium">Medium</option>
                                        <option value="Low">Low</option>
                                      </select>                                    
                                    </div>
                                    <div class="form-group col-md-4">
                                    </div>
                                  </div>                                  
                                  <button type="submit" class="btn btn-primary">Submit</button>
                                </form>                                
                        </div>
                </body>
                </html>'''
                
if __name__ == '__main__':
    model_columns = joblib.load("ColumnsPickle.pkl")
    print ('Model columns loaded')
    lr = joblib.load("RandomForestPickle.pkl")
    print ('Model loaded')
    app.run(port = 12345)
