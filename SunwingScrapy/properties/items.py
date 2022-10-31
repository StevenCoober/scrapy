import scrapy
import os, sys, glob, random, traceback, json
def enum(**enums):
    return type('Enum', (), enums)
FlightType = enum(
    ONEWAY=0,
    ROUNDTRIP=1,
)
TicketType = enum(
    Regular=0,
    Flexible=1,
    Full=2,
)
"""<Ticket>票据"""
class Ticket(scrapy.Item):
    ticketType = scrapy.Field()
    resultatsAller = scrapy.Field()
    price = scrapy.Field()
    has_hoverover = scrapy.Field()
    def init(self):
        self["ticketType"] = 0
        self["resultatsAller"] = ""
        self["price"] = ""
        self["has_hoverover"] = False
    def clone(self):
        obj = Ticket()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = Ticket()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'ticketType': self["ticketType"],
            'price': self["price"],
        }
    def serializeAll(self):
        return {
            'ticketType': self["ticketType"],
            'resultatsAller': self["resultatsAller"],
            'price': self["price"],
            'has_hoverover': self["has_hoverover"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if Ticket.formatcb: return Ticket.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            Ticket.joinstr.join(vnames)+Ticket.joinstr+'ticketType': str(self["ticketType"]),
            Ticket.joinstr.join(vnames)+Ticket.joinstr+'price': str(self["price"]),
        }
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'ticketType' in data:
            self["ticketType"] = data['ticketType']
        if 'resultatsAller' in data:
            self["resultatsAller"] = data['resultatsAller']
        if 'price' in data:
            self["price"] = data['price']
        if 'has_hoverover' in data:
            self["has_hoverover"] = data['has_hoverover']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'ticketType' in data:
            self["ticketType"] = data['ticketType']
        if 'price' in data:
            self["price"] = data['price']
"""<AirportInfo>机场信息"""
class AirportInfo(scrapy.Item):
    code = scrapy.Field()
    countryId = scrapy.Field()
    airportName = scrapy.Field()
    countryName = scrapy.Field()
    countryCode = scrapy.Field()
    countryChineaseName = scrapy.Field()
    def init(self):
        self["code"] = ""
        self["countryId"] = ""
        self["airportName"] = ""
        self["countryName"] = ""
        self["countryCode"] = ""
        self["countryChineaseName"] = ""
    def clone(self):
        obj = AirportInfo()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = AirportInfo()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'code': self["code"],
            'countryId': self["countryId"],
            'airportName': self["airportName"],
            'countryName': self["countryName"],
            'countryCode': self["countryCode"],
            'countryChineaseName': self["countryChineaseName"],
        }
    def serializeAll(self):
        return {
            'code': self["code"],
            'countryId': self["countryId"],
            'airportName': self["airportName"],
            'countryName': self["countryName"],
            'countryCode': self["countryCode"],
            'countryChineaseName': self["countryChineaseName"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if AirportInfo.formatcb: return AirportInfo.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            AirportInfo.joinstr.join(vnames)+AirportInfo.joinstr+'code': str(self["code"]),
            AirportInfo.joinstr.join(vnames)+AirportInfo.joinstr+'countryId': str(self["countryId"]),
            AirportInfo.joinstr.join(vnames)+AirportInfo.joinstr+'airportName': str(self["airportName"]),
            AirportInfo.joinstr.join(vnames)+AirportInfo.joinstr+'countryName': str(self["countryName"]),
            AirportInfo.joinstr.join(vnames)+AirportInfo.joinstr+'countryCode': str(self["countryCode"]),
            AirportInfo.joinstr.join(vnames)+AirportInfo.joinstr+'countryChineaseName': str(self["countryChineaseName"]),
        }
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'code' in data:
            self["code"] = data['code']
        if 'countryId' in data:
            self["countryId"] = data['countryId']
        if 'airportName' in data:
            self["airportName"] = data['airportName']
        if 'countryName' in data:
            self["countryName"] = data['countryName']
        if 'countryCode' in data:
            self["countryCode"] = data['countryCode']
        if 'countryChineaseName' in data:
            self["countryChineaseName"] = data['countryChineaseName']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'code' in data:
            self["code"] = data['code']
        if 'countryId' in data:
            self["countryId"] = data['countryId']
        if 'airportName' in data:
            self["airportName"] = data['airportName']
        if 'countryName' in data:
            self["countryName"] = data['countryName']
        if 'countryCode' in data:
            self["countryCode"] = data['countryCode']
        if 'countryChineaseName' in data:
            self["countryChineaseName"] = data['countryChineaseName']
"""<Fee>一项费用"""
class Fee(scrapy.Item):
    feeName = scrapy.Field()
    feePrice = scrapy.Field()
    def init(self):
        self["feeName"] = ""
        self["feePrice"] = ""
    def clone(self):
        obj = Fee()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = Fee()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'feeName': self["feeName"],
            'feePrice': self["feePrice"],
        }
    def serializeAll(self):
        return {
            'feeName': self["feeName"],
            'feePrice': self["feePrice"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if Fee.formatcb: return Fee.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            Fee.joinstr.join(vnames)+Fee.joinstr+'feeName': str(self["feeName"]),
            Fee.joinstr.join(vnames)+Fee.joinstr+'feePrice': str(self["feePrice"]),
        }
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'feeName' in data:
            self["feeName"] = data['feeName']
        if 'feePrice' in data:
            self["feePrice"] = data['feePrice']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'feeName' in data:
            self["feeName"] = data['feeName']
        if 'feePrice' in data:
            self["feePrice"] = data['feePrice']
"""<Flight>来回航班"""
class Flight(scrapy.Item):
    flightName = scrapy.Field()
    planeName = scrapy.Field()
    originCityName = scrapy.Field()
    destinationCityName = scrapy.Field()
    allTickets = scrapy.Field()
    chooseTicket = scrapy.Field()
    Itinerary = scrapy.Field()
    time_dep = scrapy.Field()
    time_arr = scrapy.Field()
    duration = scrapy.Field()
    Fromdate = scrapy.Field()
    Todate = scrapy.Field()
    Nb_seats_for_ajax0 = scrapy.Field()
    def init(self):
        self["flightName"] = ""
        self["planeName"] = ""
        self["originCityName"] = ""
        self["destinationCityName"] = ""
        self["allTickets"] = []
        self["chooseTicket"] = Ticket()
        self["chooseTicket"].init() 
        self["Itinerary"] = ""
        self["time_dep"] = ""
        self["time_arr"] = ""
        self["duration"] = ""
        self["Fromdate"] = ""
        self["Todate"] = ""
        self["Nb_seats_for_ajax0"] = ""
    def clone(self):
        obj = Flight()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = Flight()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'flightName': self["flightName"],
            'planeName': self["planeName"],
            'chooseTicket': self["chooseTicket"].serialize(),
            'time_dep': self["time_dep"],
            'time_arr': self["time_arr"],
            'duration': self["duration"],
            'Fromdate': self["Fromdate"],
            'Todate': self["Todate"],
            'Nb_seats_for_ajax0': self["Nb_seats_for_ajax0"],
        }
    def serializeAll(self):
        return {
            'flightName': self["flightName"],
            'planeName': self["planeName"],
            'originCityName': self["originCityName"],
            'destinationCityName': self["destinationCityName"],
            'allTickets': [x.serializeAll() for x in self["allTickets"]],
            'chooseTicket': self["chooseTicket"].serializeAll(),
            'Itinerary': self["Itinerary"],
            'time_dep': self["time_dep"],
            'time_arr': self["time_arr"],
            'duration': self["duration"],
            'Fromdate': self["Fromdate"],
            'Todate': self["Todate"],
            'Nb_seats_for_ajax0': self["Nb_seats_for_ajax0"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if Flight.formatcb: return Flight.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            Flight.joinstr.join(vnames)+Flight.joinstr+'flightName': str(self["flightName"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'planeName': str(self["planeName"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'time_dep': str(self["time_dep"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'time_arr': str(self["time_arr"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'duration': str(self["duration"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'Fromdate': str(self["Fromdate"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'Todate': str(self["Todate"]),
            Flight.joinstr.join(vnames)+Flight.joinstr+'Nb_seats_for_ajax0': str(self["Nb_seats_for_ajax0"]),
        }
        _chooseTicket_ = self["chooseTicket"].serializeFormat__(vnames+["chooseTicket"])
        if isinstance(_chooseTicket_, dict):_map.update(_chooseTicket_)
        elif isinstance(_chooseTicket_, str): _map['chooseTicket'] = _chooseTicket_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightName' in data:
            self["flightName"] = data['flightName']
        if 'planeName' in data:
            self["planeName"] = data['planeName']
        if 'originCityName' in data:
            self["originCityName"] = data['originCityName']
        if 'destinationCityName' in data:
            self["destinationCityName"] = data['destinationCityName']
        if 'allTickets' in data:
            for x in data['allTickets']:
                _ticket = Ticket()
                _ticket.deserializeAll(x)
                self["allTickets"].append(_ticket)
        if 'chooseTicket' in data:
            _ticket = Ticket()
            _ticket.deserializeAll(data['chooseTicket'])
            self["chooseTicket"] = _ticket
        if 'Itinerary' in data:
            self["Itinerary"] = data['Itinerary']
        if 'time_dep' in data:
            self["time_dep"] = data['time_dep']
        if 'time_arr' in data:
            self["time_arr"] = data['time_arr']
        if 'duration' in data:
            self["duration"] = data['duration']
        if 'Fromdate' in data:
            self["Fromdate"] = data['Fromdate']
        if 'Todate' in data:
            self["Todate"] = data['Todate']
        if 'Nb_seats_for_ajax0' in data:
            self["Nb_seats_for_ajax0"] = data['Nb_seats_for_ajax0']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightName' in data:
            self["flightName"] = data['flightName']
        if 'planeName' in data:
            self["planeName"] = data['planeName']
        if 'chooseTicket' in data:
            _ticket = Ticket()
            _ticket.deserialize(data['chooseTicket'])
            self["chooseTicket"] = _ticket
        if 'time_dep' in data:
            self["time_dep"] = data['time_dep']
        if 'time_arr' in data:
            self["time_arr"] = data['time_arr']
        if 'duration' in data:
            self["duration"] = data['duration']
        if 'Fromdate' in data:
            self["Fromdate"] = data['Fromdate']
        if 'Todate' in data:
            self["Todate"] = data['Todate']
        if 'Nb_seats_for_ajax0' in data:
            self["Nb_seats_for_ajax0"] = data['Nb_seats_for_ajax0']
"""<FormData>表单数据"""
class FormData(scrapy.Item):
    sid = scrapy.Field()
    def init(self):
        self["sid"] = ""
    def clone(self):
        obj = FormData()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = FormData()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'sid': self["sid"],
        }
    def serializeAll(self):
        return {
            'sid': self["sid"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if FormData.formatcb: return FormData.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            FormData.joinstr.join(vnames)+FormData.joinstr+'sid': str(self["sid"]),
        }
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'sid' in data:
            self["sid"] = data['sid']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'sid' in data:
            self["sid"] = data['sid']
"""<RoundtripFlight>往返"""
class RoundtripFlight(scrapy.Item):
    flightType = scrapy.Field()
    origin = scrapy.Field()
    destinations = scrapy.Field()
    def init(self):
        self["flightType"] = 1
        self["origin"] = AirportInfo()
        self["origin"].init() 
        self["destinations"] = []
    def clone(self):
        obj = RoundtripFlight()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = RoundtripFlight()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'origin': self["origin"].serialize(),
            'destinations': [x.serialize() for x in self["destinations"]],
        }
    def serializeAll(self):
        return {
            'flightType': self["flightType"],
            'origin': self["origin"].serializeAll(),
            'destinations': [x.serializeAll() for x in self["destinations"]],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if RoundtripFlight.formatcb: return RoundtripFlight.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
        }
        _origin_ = self["origin"].serializeFormat__(vnames+["origin"])
        if isinstance(_origin_, dict):_map.update(_origin_)
        elif isinstance(_origin_, str): _map['origin'] = _origin_
        _destinations_ = {}
        if AirportInfo.formatcb: 
            _r = AirportInfo.formatcb(self["destinations"], vnames + ["destinations"])
            if isinstance(_r, dict):_destinations_.update(_r)
            elif isinstance(_r, str): _destinations_["destinations"] = _r
        else:
            for i, e in enumerate(self["destinations"]):
                _r = e.serializeFormat__(vnames+["destinations" + RoundtripFlight.joinstr + str(i)])
                if isinstance(_r, dict):_destinations_.update(_r)
                elif isinstance(_r, str): _destinations_["destinations" + RoundtripFlight.joinstr + str(i)] = _r
        if isinstance(_destinations_, dict):_map.update(_destinations_)
        elif isinstance(_destinations_, str): _map['destinations'] = _destinations_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightType' in data:
            self["flightType"] = data['flightType']
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserializeAll(data['origin'])
            self["origin"] = _airportInfo
        if 'destinations' in data:
            for x in data['destinations']:
                _airportInfo = AirportInfo()
                _airportInfo.deserializeAll(x)
                self["destinations"].append(_airportInfo)
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserialize(data['origin'])
            self["origin"] = _airportInfo
        if 'destinations' in data:
            for x in data['destinations']:
                _airportInfo = AirportInfo()
                _airportInfo.deserialize(x)
                self["destinations"].append(_airportInfo)
"""<OnewayFlight>单程"""
class OnewayFlight(scrapy.Item):
    flightType = scrapy.Field()
    origin = scrapy.Field()
    destinations = scrapy.Field()
    def init(self):
        self["flightType"] = 0
        self["origin"] = AirportInfo()
        self["origin"].init() 
        self["destinations"] = []
    def clone(self):
        obj = OnewayFlight()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = OnewayFlight()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'origin': self["origin"].serialize(),
            'destinations': [x.serialize() for x in self["destinations"]],
        }
    def serializeAll(self):
        return {
            'flightType': self["flightType"],
            'origin': self["origin"].serializeAll(),
            'destinations': [x.serializeAll() for x in self["destinations"]],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if OnewayFlight.formatcb: return OnewayFlight.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
        }
        _origin_ = self["origin"].serializeFormat__(vnames+["origin"])
        if isinstance(_origin_, dict):_map.update(_origin_)
        elif isinstance(_origin_, str): _map['origin'] = _origin_
        _destinations_ = {}
        if AirportInfo.formatcb: 
            _r = AirportInfo.formatcb(self["destinations"], vnames + ["destinations"])
            if isinstance(_r, dict):_destinations_.update(_r)
            elif isinstance(_r, str): _destinations_["destinations"] = _r
        else:
            for i, e in enumerate(self["destinations"]):
                _r = e.serializeFormat__(vnames+["destinations" + OnewayFlight.joinstr + str(i)])
                if isinstance(_r, dict):_destinations_.update(_r)
                elif isinstance(_r, str): _destinations_["destinations" + OnewayFlight.joinstr + str(i)] = _r
        if isinstance(_destinations_, dict):_map.update(_destinations_)
        elif isinstance(_destinations_, str): _map['destinations'] = _destinations_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightType' in data:
            self["flightType"] = data['flightType']
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserializeAll(data['origin'])
            self["origin"] = _airportInfo
        if 'destinations' in data:
            for x in data['destinations']:
                _airportInfo = AirportInfo()
                _airportInfo.deserializeAll(x)
                self["destinations"].append(_airportInfo)
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserialize(data['origin'])
            self["origin"] = _airportInfo
        if 'destinations' in data:
            for x in data['destinations']:
                _airportInfo = AirportInfo()
                _airportInfo.deserialize(x)
                self["destinations"].append(_airportInfo)
"""<FlightChooseDate>选择飞行时间"""
class FlightChooseDate(scrapy.Item):
    flightType = scrapy.Field()
    origin = scrapy.Field()
    destination = scrapy.Field()
    fromDate = scrapy.Field()
    availableFromDates = scrapy.Field()
    selectFromDate = scrapy.Field()
    returnDate = scrapy.Field()
    availableReturnDates = scrapy.Field()
    selectReturnDate = scrapy.Field()
    formData = scrapy.Field()
    departingFlights = scrapy.Field()
    chooseDepartingFlight = scrapy.Field()
    returningFlights = scrapy.Field()
    chooseReturningFlight = scrapy.Field()
    Upgrade_Your_Experience = scrapy.Field()
    Protect_Your_Vacation = scrapy.Field()
    Airport_Lounge = scrapy.Field()
    Excursions = scrapy.Field()
    Air_Transportation_Charges = scrapy.Field()
    Surcharges = scrapy.Field()
    Taxes_Fees_And_Charges = scrapy.Field()
    Td_Pricetotal = scrapy.Field()
    def init(self):
        self["flightType"] = 0
        self["origin"] = AirportInfo()
        self["origin"].init() 
        self["destination"] = AirportInfo()
        self["destination"].init() 
        self["fromDate"] = ""
        self["availableFromDates"] = []
        self["selectFromDate"] = ""
        self["returnDate"] = ""
        self["availableReturnDates"] = []
        self["selectReturnDate"] = ""
        self["formData"] = FormData()
        self["formData"].init() 
        self["departingFlights"] = []
        self["chooseDepartingFlight"] = Flight()
        self["chooseDepartingFlight"].init() 
        self["returningFlights"] = []
        self["chooseReturningFlight"] = Flight()
        self["chooseReturningFlight"].init() 
        self["Upgrade_Your_Experience"] = []
        self["Protect_Your_Vacation"] = []
        self["Airport_Lounge"] = []
        self["Excursions"] = []
        self["Air_Transportation_Charges"] = ""
        self["Surcharges"] = ""
        self["Taxes_Fees_And_Charges"] = ""
        self["Td_Pricetotal"] = ""
    def clone(self):
        obj = FlightChooseDate()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = FlightChooseDate()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'flightType': self["flightType"],
            'origin': self["origin"].serialize(),
            'destination': self["destination"].serialize(),
            'selectFromDate': self["selectFromDate"],
            'selectReturnDate': self["selectReturnDate"],
            'chooseDepartingFlight': self["chooseDepartingFlight"].serialize(),
            'chooseReturningFlight': self["chooseReturningFlight"].serialize(),
            'Upgrade_Your_Experience': [x.serialize() for x in self["Upgrade_Your_Experience"]],
            'Protect_Your_Vacation': [x.serialize() for x in self["Protect_Your_Vacation"]],
            'Airport_Lounge': [x.serialize() for x in self["Airport_Lounge"]],
            'Excursions': [x.serialize() for x in self["Excursions"]],
            'Air_Transportation_Charges': self["Air_Transportation_Charges"],
            'Surcharges': self["Surcharges"],
            'Taxes_Fees_And_Charges': self["Taxes_Fees_And_Charges"],
            'Td_Pricetotal': self["Td_Pricetotal"],
        }
    def serializeAll(self):
        return {
            'flightType': self["flightType"],
            'origin': self["origin"].serializeAll(),
            'destination': self["destination"].serializeAll(),
            'fromDate': self["fromDate"],
            'availableFromDates': self["availableFromDates"],
            'selectFromDate': self["selectFromDate"],
            'returnDate': self["returnDate"],
            'availableReturnDates': self["availableReturnDates"],
            'selectReturnDate': self["selectReturnDate"],
            'formData': self["formData"].serializeAll(),
            'departingFlights': [x.serializeAll() for x in self["departingFlights"]],
            'chooseDepartingFlight': self["chooseDepartingFlight"].serializeAll(),
            'returningFlights': [x.serializeAll() for x in self["returningFlights"]],
            'chooseReturningFlight': self["chooseReturningFlight"].serializeAll(),
            'Upgrade_Your_Experience': [x.serializeAll() for x in self["Upgrade_Your_Experience"]],
            'Protect_Your_Vacation': [x.serializeAll() for x in self["Protect_Your_Vacation"]],
            'Airport_Lounge': [x.serializeAll() for x in self["Airport_Lounge"]],
            'Excursions': [x.serializeAll() for x in self["Excursions"]],
            'Air_Transportation_Charges': self["Air_Transportation_Charges"],
            'Surcharges': self["Surcharges"],
            'Taxes_Fees_And_Charges': self["Taxes_Fees_And_Charges"],
            'Td_Pricetotal': self["Td_Pricetotal"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if FlightChooseDate.formatcb: return FlightChooseDate.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'flightType': str(self["flightType"]),
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'selectFromDate': str(self["selectFromDate"]),
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'selectReturnDate': str(self["selectReturnDate"]),
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'Air_Transportation_Charges': str(self["Air_Transportation_Charges"]),
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'Surcharges': str(self["Surcharges"]),
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'Taxes_Fees_And_Charges': str(self["Taxes_Fees_And_Charges"]),
            FlightChooseDate.joinstr.join(vnames)+FlightChooseDate.joinstr+'Td_Pricetotal': str(self["Td_Pricetotal"]),
        }
        _origin_ = self["origin"].serializeFormat__(vnames+["origin"])
        if isinstance(_origin_, dict):_map.update(_origin_)
        elif isinstance(_origin_, str): _map['origin'] = _origin_
        _destination_ = self["destination"].serializeFormat__(vnames+["destination"])
        if isinstance(_destination_, dict):_map.update(_destination_)
        elif isinstance(_destination_, str): _map['destination'] = _destination_
        _chooseDepartingFlight_ = self["chooseDepartingFlight"].serializeFormat__(vnames+["chooseDepartingFlight"])
        if isinstance(_chooseDepartingFlight_, dict):_map.update(_chooseDepartingFlight_)
        elif isinstance(_chooseDepartingFlight_, str): _map['chooseDepartingFlight'] = _chooseDepartingFlight_
        _chooseReturningFlight_ = self["chooseReturningFlight"].serializeFormat__(vnames+["chooseReturningFlight"])
        if isinstance(_chooseReturningFlight_, dict):_map.update(_chooseReturningFlight_)
        elif isinstance(_chooseReturningFlight_, str): _map['chooseReturningFlight'] = _chooseReturningFlight_
        _Upgrade_Your_Experience_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Upgrade_Your_Experience"], vnames + ["Upgrade_Your_Experience"])
            if isinstance(_r, dict):_Upgrade_Your_Experience_.update(_r)
            elif isinstance(_r, str): _Upgrade_Your_Experience_["Upgrade_Your_Experience"] = _r
        else:
            for i, e in enumerate(self["Upgrade_Your_Experience"]):
                _r = e.serializeFormat__(vnames+["Upgrade_Your_Experience" + FlightChooseDate.joinstr + str(i)])
                if isinstance(_r, dict):_Upgrade_Your_Experience_.update(_r)
                elif isinstance(_r, str): _Upgrade_Your_Experience_["Upgrade_Your_Experience" + FlightChooseDate.joinstr + str(i)] = _r
        if isinstance(_Upgrade_Your_Experience_, dict):_map.update(_Upgrade_Your_Experience_)
        elif isinstance(_Upgrade_Your_Experience_, str): _map['Upgrade_Your_Experience'] = _Upgrade_Your_Experience_
        _Protect_Your_Vacation_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Protect_Your_Vacation"], vnames + ["Protect_Your_Vacation"])
            if isinstance(_r, dict):_Protect_Your_Vacation_.update(_r)
            elif isinstance(_r, str): _Protect_Your_Vacation_["Protect_Your_Vacation"] = _r
        else:
            for i, e in enumerate(self["Protect_Your_Vacation"]):
                _r = e.serializeFormat__(vnames+["Protect_Your_Vacation" + FlightChooseDate.joinstr + str(i)])
                if isinstance(_r, dict):_Protect_Your_Vacation_.update(_r)
                elif isinstance(_r, str): _Protect_Your_Vacation_["Protect_Your_Vacation" + FlightChooseDate.joinstr + str(i)] = _r
        if isinstance(_Protect_Your_Vacation_, dict):_map.update(_Protect_Your_Vacation_)
        elif isinstance(_Protect_Your_Vacation_, str): _map['Protect_Your_Vacation'] = _Protect_Your_Vacation_
        _Airport_Lounge_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Airport_Lounge"], vnames + ["Airport_Lounge"])
            if isinstance(_r, dict):_Airport_Lounge_.update(_r)
            elif isinstance(_r, str): _Airport_Lounge_["Airport_Lounge"] = _r
        else:
            for i, e in enumerate(self["Airport_Lounge"]):
                _r = e.serializeFormat__(vnames+["Airport_Lounge" + FlightChooseDate.joinstr + str(i)])
                if isinstance(_r, dict):_Airport_Lounge_.update(_r)
                elif isinstance(_r, str): _Airport_Lounge_["Airport_Lounge" + FlightChooseDate.joinstr + str(i)] = _r
        if isinstance(_Airport_Lounge_, dict):_map.update(_Airport_Lounge_)
        elif isinstance(_Airport_Lounge_, str): _map['Airport_Lounge'] = _Airport_Lounge_
        _Excursions_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Excursions"], vnames + ["Excursions"])
            if isinstance(_r, dict):_Excursions_.update(_r)
            elif isinstance(_r, str): _Excursions_["Excursions"] = _r
        else:
            for i, e in enumerate(self["Excursions"]):
                _r = e.serializeFormat__(vnames+["Excursions" + FlightChooseDate.joinstr + str(i)])
                if isinstance(_r, dict):_Excursions_.update(_r)
                elif isinstance(_r, str): _Excursions_["Excursions" + FlightChooseDate.joinstr + str(i)] = _r
        if isinstance(_Excursions_, dict):_map.update(_Excursions_)
        elif isinstance(_Excursions_, str): _map['Excursions'] = _Excursions_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightType' in data:
            self["flightType"] = data['flightType']
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserializeAll(data['origin'])
            self["origin"] = _airportInfo
        if 'destination' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserializeAll(data['destination'])
            self["destination"] = _airportInfo
        if 'fromDate' in data:
            self["fromDate"] = data['fromDate']
        if 'availableFromDates' in data:
            self["availableFromDates"] = data['availableFromDates']
        if 'selectFromDate' in data:
            self["selectFromDate"] = data['selectFromDate']
        if 'returnDate' in data:
            self["returnDate"] = data['returnDate']
        if 'availableReturnDates' in data:
            self["availableReturnDates"] = data['availableReturnDates']
        if 'selectReturnDate' in data:
            self["selectReturnDate"] = data['selectReturnDate']
        if 'formData' in data:
            _formData = FormData()
            _formData.deserializeAll(data['formData'])
            self["formData"] = _formData
        if 'departingFlights' in data:
            for x in data['departingFlights']:
                _flight = Flight()
                _flight.deserializeAll(x)
                self["departingFlights"].append(_flight)
        if 'chooseDepartingFlight' in data:
            _flight = Flight()
            _flight.deserializeAll(data['chooseDepartingFlight'])
            self["chooseDepartingFlight"] = _flight
        if 'returningFlights' in data:
            for x in data['returningFlights']:
                _flight = Flight()
                _flight.deserializeAll(x)
                self["returningFlights"].append(_flight)
        if 'chooseReturningFlight' in data:
            _flight = Flight()
            _flight.deserializeAll(data['chooseReturningFlight'])
            self["chooseReturningFlight"] = _flight
        if 'Upgrade_Your_Experience' in data:
            for x in data['Upgrade_Your_Experience']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Upgrade_Your_Experience"].append(_fee)
        if 'Protect_Your_Vacation' in data:
            for x in data['Protect_Your_Vacation']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Protect_Your_Vacation"].append(_fee)
        if 'Airport_Lounge' in data:
            for x in data['Airport_Lounge']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Airport_Lounge"].append(_fee)
        if 'Excursions' in data:
            for x in data['Excursions']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Excursions"].append(_fee)
        if 'Air_Transportation_Charges' in data:
            self["Air_Transportation_Charges"] = data['Air_Transportation_Charges']
        if 'Surcharges' in data:
            self["Surcharges"] = data['Surcharges']
        if 'Taxes_Fees_And_Charges' in data:
            self["Taxes_Fees_And_Charges"] = data['Taxes_Fees_And_Charges']
        if 'Td_Pricetotal' in data:
            self["Td_Pricetotal"] = data['Td_Pricetotal']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightType' in data:
            self["flightType"] = data['flightType']
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserialize(data['origin'])
            self["origin"] = _airportInfo
        if 'destination' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserialize(data['destination'])
            self["destination"] = _airportInfo
        if 'selectFromDate' in data:
            self["selectFromDate"] = data['selectFromDate']
        if 'selectReturnDate' in data:
            self["selectReturnDate"] = data['selectReturnDate']
        if 'chooseDepartingFlight' in data:
            _flight = Flight()
            _flight.deserialize(data['chooseDepartingFlight'])
            self["chooseDepartingFlight"] = _flight
        if 'chooseReturningFlight' in data:
            _flight = Flight()
            _flight.deserialize(data['chooseReturningFlight'])
            self["chooseReturningFlight"] = _flight
        if 'Upgrade_Your_Experience' in data:
            for x in data['Upgrade_Your_Experience']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Upgrade_Your_Experience"].append(_fee)
        if 'Protect_Your_Vacation' in data:
            for x in data['Protect_Your_Vacation']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Protect_Your_Vacation"].append(_fee)
        if 'Airport_Lounge' in data:
            for x in data['Airport_Lounge']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Airport_Lounge"].append(_fee)
        if 'Excursions' in data:
            for x in data['Excursions']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Excursions"].append(_fee)
        if 'Air_Transportation_Charges' in data:
            self["Air_Transportation_Charges"] = data['Air_Transportation_Charges']
        if 'Surcharges' in data:
            self["Surcharges"] = data['Surcharges']
        if 'Taxes_Fees_And_Charges' in data:
            self["Taxes_Fees_And_Charges"] = data['Taxes_Fees_And_Charges']
        if 'Td_Pricetotal' in data:
            self["Td_Pricetotal"] = data['Td_Pricetotal']
"""<AirportCountryInfo>机场国家固定信息"""
class AirportCountryInfo(scrapy.Item):
    code = scrapy.Field()
    countryCode = scrapy.Field()
    countryChineaseName = scrapy.Field()
    def init(self):
        self["code"] = ""
        self["countryCode"] = ""
        self["countryChineaseName"] = ""
    def clone(self):
        obj = AirportCountryInfo()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = AirportCountryInfo()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'code': self["code"],
            'countryCode': self["countryCode"],
            'countryChineaseName': self["countryChineaseName"],
        }
    def serializeAll(self):
        return {
            'code': self["code"],
            'countryCode': self["countryCode"],
            'countryChineaseName': self["countryChineaseName"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if AirportCountryInfo.formatcb: return AirportCountryInfo.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            AirportCountryInfo.joinstr.join(vnames)+AirportCountryInfo.joinstr+'code': str(self["code"]),
            AirportCountryInfo.joinstr.join(vnames)+AirportCountryInfo.joinstr+'countryCode': str(self["countryCode"]),
            AirportCountryInfo.joinstr.join(vnames)+AirportCountryInfo.joinstr+'countryChineaseName': str(self["countryChineaseName"]),
        }
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'code' in data:
            self["code"] = data['code']
        if 'countryCode' in data:
            self["countryCode"] = data['countryCode']
        if 'countryChineaseName' in data:
            self["countryChineaseName"] = data['countryChineaseName']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'code' in data:
            self["code"] = data['code']
        if 'countryCode' in data:
            self["countryCode"] = data['countryCode']
        if 'countryChineaseName' in data:
            self["countryChineaseName"] = data['countryChineaseName']
"""<SunwingInfo>所有信息"""
class SunwingInfo(scrapy.Item):
    oneways = scrapy.Field()
    roundtrips = scrapy.Field()
    def init(self):
        self["oneways"] = []
        self["roundtrips"] = []
    def clone(self):
        obj = SunwingInfo()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = SunwingInfo()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'oneways': [x.serialize() for x in self["oneways"]],
            'roundtrips': [x.serialize() for x in self["roundtrips"]],
        }
    def serializeAll(self):
        return {
            'oneways': [x.serializeAll() for x in self["oneways"]],
            'roundtrips': [x.serializeAll() for x in self["roundtrips"]],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if SunwingInfo.formatcb: return SunwingInfo.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
        }
        _oneways_ = {}
        if OnewayFlight.formatcb: 
            _r = OnewayFlight.formatcb(self["oneways"], vnames + ["oneways"])
            if isinstance(_r, dict):_oneways_.update(_r)
            elif isinstance(_r, str): _oneways_["oneways"] = _r
        else:
            for i, e in enumerate(self["oneways"]):
                _r = e.serializeFormat__(vnames+["oneways" + SunwingInfo.joinstr + str(i)])
                if isinstance(_r, dict):_oneways_.update(_r)
                elif isinstance(_r, str): _oneways_["oneways" + SunwingInfo.joinstr + str(i)] = _r
        if isinstance(_oneways_, dict):_map.update(_oneways_)
        elif isinstance(_oneways_, str): _map['oneways'] = _oneways_
        _roundtrips_ = {}
        if RoundtripFlight.formatcb: 
            _r = RoundtripFlight.formatcb(self["roundtrips"], vnames + ["roundtrips"])
            if isinstance(_r, dict):_roundtrips_.update(_r)
            elif isinstance(_r, str): _roundtrips_["roundtrips"] = _r
        else:
            for i, e in enumerate(self["roundtrips"]):
                _r = e.serializeFormat__(vnames+["roundtrips" + SunwingInfo.joinstr + str(i)])
                if isinstance(_r, dict):_roundtrips_.update(_r)
                elif isinstance(_r, str): _roundtrips_["roundtrips" + SunwingInfo.joinstr + str(i)] = _r
        if isinstance(_roundtrips_, dict):_map.update(_roundtrips_)
        elif isinstance(_roundtrips_, str): _map['roundtrips'] = _roundtrips_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'oneways' in data:
            for x in data['oneways']:
                _onewayFlight = OnewayFlight()
                _onewayFlight.deserializeAll(x)
                self["oneways"].append(_onewayFlight)
        if 'roundtrips' in data:
            for x in data['roundtrips']:
                _roundtripFlight = RoundtripFlight()
                _roundtripFlight.deserializeAll(x)
                self["roundtrips"].append(_roundtripFlight)
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'oneways' in data:
            for x in data['oneways']:
                _onewayFlight = OnewayFlight()
                _onewayFlight.deserialize(x)
                self["oneways"].append(_onewayFlight)
        if 'roundtrips' in data:
            for x in data['roundtrips']:
                _roundtripFlight = RoundtripFlight()
                _roundtripFlight.deserialize(x)
                self["roundtrips"].append(_roundtripFlight)
"""<ConstAirportCountryInfo>所有机场国家固定信息"""
class ConstAirportCountryInfo(scrapy.Item):
    airportCountryInfos = scrapy.Field()
    def init(self):
        self["airportCountryInfos"] = []
    def clone(self):
        obj = ConstAirportCountryInfo()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = ConstAirportCountryInfo()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'airportCountryInfos': [x.serialize() for x in self["airportCountryInfos"]],
        }
    def serializeAll(self):
        return {
            'airportCountryInfos': [x.serializeAll() for x in self["airportCountryInfos"]],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if ConstAirportCountryInfo.formatcb: return ConstAirportCountryInfo.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
        }
        _airportCountryInfos_ = {}
        if AirportCountryInfo.formatcb: 
            _r = AirportCountryInfo.formatcb(self["airportCountryInfos"], vnames + ["airportCountryInfos"])
            if isinstance(_r, dict):_airportCountryInfos_.update(_r)
            elif isinstance(_r, str): _airportCountryInfos_["airportCountryInfos"] = _r
        else:
            for i, e in enumerate(self["airportCountryInfos"]):
                _r = e.serializeFormat__(vnames+["airportCountryInfos" + ConstAirportCountryInfo.joinstr + str(i)])
                if isinstance(_r, dict):_airportCountryInfos_.update(_r)
                elif isinstance(_r, str): _airportCountryInfos_["airportCountryInfos" + ConstAirportCountryInfo.joinstr + str(i)] = _r
        if isinstance(_airportCountryInfos_, dict):_map.update(_airportCountryInfos_)
        elif isinstance(_airportCountryInfos_, str): _map['airportCountryInfos'] = _airportCountryInfos_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'airportCountryInfos' in data:
            for x in data['airportCountryInfos']:
                _airportCountryInfo = AirportCountryInfo()
                _airportCountryInfo.deserializeAll(x)
                self["airportCountryInfos"].append(_airportCountryInfo)
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'airportCountryInfos' in data:
            for x in data['airportCountryInfos']:
                _airportCountryInfo = AirportCountryInfo()
                _airportCountryInfo.deserialize(x)
                self["airportCountryInfos"].append(_airportCountryInfo)
"""<Chooses>"""
class Chooses(scrapy.Item):
    flightChooseDates = scrapy.Field()
    def init(self):
        self["flightChooseDates"] = []
    def clone(self):
        obj = Chooses()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = Chooses()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'flightChooseDates': [x.serialize() for x in self["flightChooseDates"]],
        }
    def serializeAll(self):
        return {
            'flightChooseDates': [x.serializeAll() for x in self["flightChooseDates"]],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if Chooses.formatcb: return Chooses.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
        }
        _flightChooseDates_ = {}
        if FlightChooseDate.formatcb: 
            _r = FlightChooseDate.formatcb(self["flightChooseDates"], vnames + ["flightChooseDates"])
            if isinstance(_r, dict):_flightChooseDates_.update(_r)
            elif isinstance(_r, str): _flightChooseDates_["flightChooseDates"] = _r
        else:
            for i, e in enumerate(self["flightChooseDates"]):
                _r = e.serializeFormat__(vnames+["flightChooseDates" + Chooses.joinstr + str(i)])
                if isinstance(_r, dict):_flightChooseDates_.update(_r)
                elif isinstance(_r, str): _flightChooseDates_["flightChooseDates" + Chooses.joinstr + str(i)] = _r
        if isinstance(_flightChooseDates_, dict):_map.update(_flightChooseDates_)
        elif isinstance(_flightChooseDates_, str): _map['flightChooseDates'] = _flightChooseDates_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightChooseDates' in data:
            for x in data['flightChooseDates']:
                _flightChooseDate = FlightChooseDate()
                _flightChooseDate.deserializeAll(x)
                self["flightChooseDates"].append(_flightChooseDate)
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightChooseDates' in data:
            for x in data['flightChooseDates']:
                _flightChooseDate = FlightChooseDate()
                _flightChooseDate.deserialize(x)
                self["flightChooseDates"].append(_flightChooseDate)
"""<FlightChooseDate_Backup>选择飞行时间"""
class FlightChooseDate_Backup(scrapy.Item):
    flightType = scrapy.Field()
    origin = scrapy.Field()
    destination = scrapy.Field()
    fromDate = scrapy.Field()
    availableFromDates = scrapy.Field()
    selectFromDate = scrapy.Field()
    returnDate = scrapy.Field()
    availableReturnDates = scrapy.Field()
    selectReturnDate = scrapy.Field()
    formData = scrapy.Field()
    planeName = scrapy.Field()
    Regular_resultatsAller = scrapy.Field()
    Regular = scrapy.Field()
    Flexible_resultatsAller = scrapy.Field()
    Flexible = scrapy.Field()
    choosePriceclassType = scrapy.Field()
    time_dep = scrapy.Field()
    time_arr = scrapy.Field()
    duration = scrapy.Field()
    Upgrade_Your_Experience = scrapy.Field()
    Protect_Your_Vacation = scrapy.Field()
    Airport_Lounge = scrapy.Field()
    Excursions = scrapy.Field()
    Fromdate = scrapy.Field()
    Todate = scrapy.Field()
    Nb_seats_for_ajax0 = scrapy.Field()
    Air_Transportation_Charges = scrapy.Field()
    Surcharges = scrapy.Field()
    Taxes_Fees_And_Charges = scrapy.Field()
    Td_Pricetotal = scrapy.Field()
    def init(self):
        self["flightType"] = 0
        self["origin"] = AirportInfo()
        self["origin"].init() 
        self["destination"] = AirportInfo()
        self["destination"].init() 
        self["fromDate"] = ""
        self["availableFromDates"] = []
        self["selectFromDate"] = ""
        self["returnDate"] = ""
        self["availableReturnDates"] = []
        self["selectReturnDate"] = ""
        self["formData"] = FormData()
        self["formData"].init() 
        self["planeName"] = ""
        self["Regular_resultatsAller"] = ""
        self["Regular"] = ""
        self["Flexible_resultatsAller"] = ""
        self["Flexible"] = ""
        self["choosePriceclassType"] = 0
        self["time_dep"] = ""
        self["time_arr"] = ""
        self["duration"] = ""
        self["Upgrade_Your_Experience"] = []
        self["Protect_Your_Vacation"] = []
        self["Airport_Lounge"] = []
        self["Excursions"] = []
        self["Fromdate"] = ""
        self["Todate"] = ""
        self["Nb_seats_for_ajax0"] = ""
        self["Air_Transportation_Charges"] = ""
        self["Surcharges"] = ""
        self["Taxes_Fees_And_Charges"] = ""
        self["Td_Pricetotal"] = ""
    def clone(self):
        obj = FlightChooseDate_Backup()
        obj.init()
        serializeData = self.serialize()
        obj.deserialize(serializeData)
        return obj
    def cloneAll(self):
        obj = FlightChooseDate_Backup()
        obj.init()
        serializeData = self.serializeAll()
        obj.deserializeAll(serializeData)
        return obj
    def jsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, indent=2, sort_keys=False, ensure_ascii=False)
    def simpleJsonDumps(self):
        serializeData = self.serialize()
        return json.dumps(serializeData, ensure_ascii=False, separators=(',',':'))
    def jsonLoads(self, jsonStr):
        return self.deserialize(json.loads(jsonStr, encoding='utf-8'))
    def serialize(self):
        return {
            'flightType': self["flightType"],
            'origin': self["origin"].serialize(),
            'destination': self["destination"].serialize(),
            'selectFromDate': self["selectFromDate"],
            'returnDate': self["returnDate"],
            'selectReturnDate': self["selectReturnDate"],
            'planeName': self["planeName"],
            'Regular': self["Regular"],
            'Flexible': self["Flexible"],
            'choosePriceclassType': self["choosePriceclassType"],
            'time_dep': self["time_dep"],
            'time_arr': self["time_arr"],
            'duration': self["duration"],
            'Upgrade_Your_Experience': [x.serialize() for x in self["Upgrade_Your_Experience"]],
            'Protect_Your_Vacation': [x.serialize() for x in self["Protect_Your_Vacation"]],
            'Airport_Lounge': [x.serialize() for x in self["Airport_Lounge"]],
            'Excursions': [x.serialize() for x in self["Excursions"]],
            'Fromdate': self["Fromdate"],
            'Todate': self["Todate"],
            'Nb_seats_for_ajax0': self["Nb_seats_for_ajax0"],
            'Air_Transportation_Charges': self["Air_Transportation_Charges"],
            'Surcharges': self["Surcharges"],
            'Taxes_Fees_And_Charges': self["Taxes_Fees_And_Charges"],
            'Td_Pricetotal': self["Td_Pricetotal"],
        }
    def serializeAll(self):
        return {
            'flightType': self["flightType"],
            'origin': self["origin"].serializeAll(),
            'destination': self["destination"].serializeAll(),
            'fromDate': self["fromDate"],
            'availableFromDates': self["availableFromDates"],
            'selectFromDate': self["selectFromDate"],
            'returnDate': self["returnDate"],
            'availableReturnDates': self["availableReturnDates"],
            'selectReturnDate': self["selectReturnDate"],
            'formData': self["formData"].serializeAll(),
            'planeName': self["planeName"],
            'Regular_resultatsAller': self["Regular_resultatsAller"],
            'Regular': self["Regular"],
            'Flexible_resultatsAller': self["Flexible_resultatsAller"],
            'Flexible': self["Flexible"],
            'choosePriceclassType': self["choosePriceclassType"],
            'time_dep': self["time_dep"],
            'time_arr': self["time_arr"],
            'duration': self["duration"],
            'Upgrade_Your_Experience': [x.serializeAll() for x in self["Upgrade_Your_Experience"]],
            'Protect_Your_Vacation': [x.serializeAll() for x in self["Protect_Your_Vacation"]],
            'Airport_Lounge': [x.serializeAll() for x in self["Airport_Lounge"]],
            'Excursions': [x.serializeAll() for x in self["Excursions"]],
            'Fromdate': self["Fromdate"],
            'Todate': self["Todate"],
            'Nb_seats_for_ajax0': self["Nb_seats_for_ajax0"],
            'Air_Transportation_Charges': self["Air_Transportation_Charges"],
            'Surcharges': self["Surcharges"],
            'Taxes_Fees_And_Charges': self["Taxes_Fees_And_Charges"],
            'Td_Pricetotal': self["Td_Pricetotal"],
        }
    formatcb = None
    joinstr = "_"
    def serializeFormat__(self, vnames=['']):
        if FlightChooseDate_Backup.formatcb: return FlightChooseDate_Backup.formatcb([self], vnames)
        return self.serializeFormat(vnames)
    def serializeFormat(self, vnames=['']):
        _map = {
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'flightType': str(self["flightType"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'selectFromDate': str(self["selectFromDate"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'returnDate': str(self["returnDate"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'selectReturnDate': str(self["selectReturnDate"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'planeName': str(self["planeName"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Regular': str(self["Regular"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Flexible': str(self["Flexible"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'choosePriceclassType': str(self["choosePriceclassType"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'time_dep': str(self["time_dep"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'time_arr': str(self["time_arr"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'duration': str(self["duration"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Fromdate': str(self["Fromdate"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Todate': str(self["Todate"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Nb_seats_for_ajax0': str(self["Nb_seats_for_ajax0"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Air_Transportation_Charges': str(self["Air_Transportation_Charges"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Surcharges': str(self["Surcharges"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Taxes_Fees_And_Charges': str(self["Taxes_Fees_And_Charges"]),
            FlightChooseDate_Backup.joinstr.join(vnames)+FlightChooseDate_Backup.joinstr+'Td_Pricetotal': str(self["Td_Pricetotal"]),
        }
        _origin_ = self["origin"].serializeFormat__(vnames+["origin"])
        if isinstance(_origin_, dict):_map.update(_origin_)
        elif isinstance(_origin_, str): _map['origin'] = _origin_
        _destination_ = self["destination"].serializeFormat__(vnames+["destination"])
        if isinstance(_destination_, dict):_map.update(_destination_)
        elif isinstance(_destination_, str): _map['destination'] = _destination_
        _Upgrade_Your_Experience_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Upgrade_Your_Experience"], vnames + ["Upgrade_Your_Experience"])
            if isinstance(_r, dict):_Upgrade_Your_Experience_.update(_r)
            elif isinstance(_r, str): _Upgrade_Your_Experience_["Upgrade_Your_Experience"] = _r
        else:
            for i, e in enumerate(self["Upgrade_Your_Experience"]):
                _r = e.serializeFormat__(vnames+["Upgrade_Your_Experience" + FlightChooseDate_Backup.joinstr + str(i)])
                if isinstance(_r, dict):_Upgrade_Your_Experience_.update(_r)
                elif isinstance(_r, str): _Upgrade_Your_Experience_["Upgrade_Your_Experience" + FlightChooseDate_Backup.joinstr + str(i)] = _r
        if isinstance(_Upgrade_Your_Experience_, dict):_map.update(_Upgrade_Your_Experience_)
        elif isinstance(_Upgrade_Your_Experience_, str): _map['Upgrade_Your_Experience'] = _Upgrade_Your_Experience_
        _Protect_Your_Vacation_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Protect_Your_Vacation"], vnames + ["Protect_Your_Vacation"])
            if isinstance(_r, dict):_Protect_Your_Vacation_.update(_r)
            elif isinstance(_r, str): _Protect_Your_Vacation_["Protect_Your_Vacation"] = _r
        else:
            for i, e in enumerate(self["Protect_Your_Vacation"]):
                _r = e.serializeFormat__(vnames+["Protect_Your_Vacation" + FlightChooseDate_Backup.joinstr + str(i)])
                if isinstance(_r, dict):_Protect_Your_Vacation_.update(_r)
                elif isinstance(_r, str): _Protect_Your_Vacation_["Protect_Your_Vacation" + FlightChooseDate_Backup.joinstr + str(i)] = _r
        if isinstance(_Protect_Your_Vacation_, dict):_map.update(_Protect_Your_Vacation_)
        elif isinstance(_Protect_Your_Vacation_, str): _map['Protect_Your_Vacation'] = _Protect_Your_Vacation_
        _Airport_Lounge_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Airport_Lounge"], vnames + ["Airport_Lounge"])
            if isinstance(_r, dict):_Airport_Lounge_.update(_r)
            elif isinstance(_r, str): _Airport_Lounge_["Airport_Lounge"] = _r
        else:
            for i, e in enumerate(self["Airport_Lounge"]):
                _r = e.serializeFormat__(vnames+["Airport_Lounge" + FlightChooseDate_Backup.joinstr + str(i)])
                if isinstance(_r, dict):_Airport_Lounge_.update(_r)
                elif isinstance(_r, str): _Airport_Lounge_["Airport_Lounge" + FlightChooseDate_Backup.joinstr + str(i)] = _r
        if isinstance(_Airport_Lounge_, dict):_map.update(_Airport_Lounge_)
        elif isinstance(_Airport_Lounge_, str): _map['Airport_Lounge'] = _Airport_Lounge_
        _Excursions_ = {}
        if Fee.formatcb: 
            _r = Fee.formatcb(self["Excursions"], vnames + ["Excursions"])
            if isinstance(_r, dict):_Excursions_.update(_r)
            elif isinstance(_r, str): _Excursions_["Excursions"] = _r
        else:
            for i, e in enumerate(self["Excursions"]):
                _r = e.serializeFormat__(vnames+["Excursions" + FlightChooseDate_Backup.joinstr + str(i)])
                if isinstance(_r, dict):_Excursions_.update(_r)
                elif isinstance(_r, str): _Excursions_["Excursions" + FlightChooseDate_Backup.joinstr + str(i)] = _r
        if isinstance(_Excursions_, dict):_map.update(_Excursions_)
        elif isinstance(_Excursions_, str): _map['Excursions'] = _Excursions_
        return _map
    def deserializeAll(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightType' in data:
            self["flightType"] = data['flightType']
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserializeAll(data['origin'])
            self["origin"] = _airportInfo
        if 'destination' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserializeAll(data['destination'])
            self["destination"] = _airportInfo
        if 'fromDate' in data:
            self["fromDate"] = data['fromDate']
        if 'availableFromDates' in data:
            self["availableFromDates"] = data['availableFromDates']
        if 'selectFromDate' in data:
            self["selectFromDate"] = data['selectFromDate']
        if 'returnDate' in data:
            self["returnDate"] = data['returnDate']
        if 'availableReturnDates' in data:
            self["availableReturnDates"] = data['availableReturnDates']
        if 'selectReturnDate' in data:
            self["selectReturnDate"] = data['selectReturnDate']
        if 'formData' in data:
            _formData = FormData()
            _formData.deserializeAll(data['formData'])
            self["formData"] = _formData
        if 'planeName' in data:
            self["planeName"] = data['planeName']
        if 'Regular_resultatsAller' in data:
            self["Regular_resultatsAller"] = data['Regular_resultatsAller']
        if 'Regular' in data:
            self["Regular"] = data['Regular']
        if 'Flexible_resultatsAller' in data:
            self["Flexible_resultatsAller"] = data['Flexible_resultatsAller']
        if 'Flexible' in data:
            self["Flexible"] = data['Flexible']
        if 'choosePriceclassType' in data:
            self["choosePriceclassType"] = data['choosePriceclassType']
        if 'time_dep' in data:
            self["time_dep"] = data['time_dep']
        if 'time_arr' in data:
            self["time_arr"] = data['time_arr']
        if 'duration' in data:
            self["duration"] = data['duration']
        if 'Upgrade_Your_Experience' in data:
            for x in data['Upgrade_Your_Experience']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Upgrade_Your_Experience"].append(_fee)
        if 'Protect_Your_Vacation' in data:
            for x in data['Protect_Your_Vacation']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Protect_Your_Vacation"].append(_fee)
        if 'Airport_Lounge' in data:
            for x in data['Airport_Lounge']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Airport_Lounge"].append(_fee)
        if 'Excursions' in data:
            for x in data['Excursions']:
                _fee = Fee()
                _fee.deserializeAll(x)
                self["Excursions"].append(_fee)
        if 'Fromdate' in data:
            self["Fromdate"] = data['Fromdate']
        if 'Todate' in data:
            self["Todate"] = data['Todate']
        if 'Nb_seats_for_ajax0' in data:
            self["Nb_seats_for_ajax0"] = data['Nb_seats_for_ajax0']
        if 'Air_Transportation_Charges' in data:
            self["Air_Transportation_Charges"] = data['Air_Transportation_Charges']
        if 'Surcharges' in data:
            self["Surcharges"] = data['Surcharges']
        if 'Taxes_Fees_And_Charges' in data:
            self["Taxes_Fees_And_Charges"] = data['Taxes_Fees_And_Charges']
        if 'Td_Pricetotal' in data:
            self["Td_Pricetotal"] = data['Td_Pricetotal']
    def deserialize(self, data:dict, hashmap:dict={}, restore_id:bool=True) -> bool:
        self.init()
        if 'flightType' in data:
            self["flightType"] = data['flightType']
        if 'origin' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserialize(data['origin'])
            self["origin"] = _airportInfo
        if 'destination' in data:
            _airportInfo = AirportInfo()
            _airportInfo.deserialize(data['destination'])
            self["destination"] = _airportInfo
        if 'selectFromDate' in data:
            self["selectFromDate"] = data['selectFromDate']
        if 'returnDate' in data:
            self["returnDate"] = data['returnDate']
        if 'selectReturnDate' in data:
            self["selectReturnDate"] = data['selectReturnDate']
        if 'planeName' in data:
            self["planeName"] = data['planeName']
        if 'Regular' in data:
            self["Regular"] = data['Regular']
        if 'Flexible' in data:
            self["Flexible"] = data['Flexible']
        if 'choosePriceclassType' in data:
            self["choosePriceclassType"] = data['choosePriceclassType']
        if 'time_dep' in data:
            self["time_dep"] = data['time_dep']
        if 'time_arr' in data:
            self["time_arr"] = data['time_arr']
        if 'duration' in data:
            self["duration"] = data['duration']
        if 'Upgrade_Your_Experience' in data:
            for x in data['Upgrade_Your_Experience']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Upgrade_Your_Experience"].append(_fee)
        if 'Protect_Your_Vacation' in data:
            for x in data['Protect_Your_Vacation']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Protect_Your_Vacation"].append(_fee)
        if 'Airport_Lounge' in data:
            for x in data['Airport_Lounge']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Airport_Lounge"].append(_fee)
        if 'Excursions' in data:
            for x in data['Excursions']:
                _fee = Fee()
                _fee.deserialize(x)
                self["Excursions"].append(_fee)
        if 'Fromdate' in data:
            self["Fromdate"] = data['Fromdate']
        if 'Todate' in data:
            self["Todate"] = data['Todate']
        if 'Nb_seats_for_ajax0' in data:
            self["Nb_seats_for_ajax0"] = data['Nb_seats_for_ajax0']
        if 'Air_Transportation_Charges' in data:
            self["Air_Transportation_Charges"] = data['Air_Transportation_Charges']
        if 'Surcharges' in data:
            self["Surcharges"] = data['Surcharges']
        if 'Taxes_Fees_And_Charges' in data:
            self["Taxes_Fees_And_Charges"] = data['Taxes_Fees_And_Charges']
        if 'Td_Pricetotal' in data:
            self["Td_Pricetotal"] = data['Td_Pricetotal']
