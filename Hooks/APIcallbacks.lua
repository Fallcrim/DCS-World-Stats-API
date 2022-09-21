local socket = require("socket")
local JSON = require("json")


local conn = socket.udp()
local test = {}
conn:settimeout(0)

function test.onSimulationStart()
    local tbl = {}
    tbl.eventName = "simulationStarted"
    local data = JSON:encode(tbl)
    conn:sendto(tostring(data), "127.0.0.1", 12000)
end

function test.onGameEvent(eventName, arg1, arg2, arg3, arg4, arg5, arg6, arg7)
    local tbl = {}
    tbl.eventName = eventName

    if eventName == "kill" then
        tbl.killerPlayerName = net.get_name(arg1)
        tbl.killerUnitType = arg2
        tbl.killerSide = arg3
        tbl.victimPlayerName = net.get_name(arg4)
        tbl.victimUnitType = arg5
        tbl.victimSide = arg6
        tbl.killerWeapon = arg7

    elseif eventName == "eject" then
        tbl.playerName = net.get_name(arg1)

    elseif eventName == "pilot_death" then
        tbl.playerName = net.get_name(arg1)

    elseif eventName == "takeoff" then
        tbl.playerName = net.get_name(arg1)

    elseif eventName == "landing" then
        tbl.playerName = net.get_name(arg1)
    end

    local data = JSON:encode(tbl)
	conn:sendto(tostring(data), "127.0.0.1", 12000)
    log.write("API HOOK", log.INFO, "Sent game event: "..eventName)
end

function test.onSimulationEnd()
    local tbl = {}
    tbl.eventName = "simulationEnded"
    local data = JSON:encode(tbl)
    conn:sendto(tostring(data), "127.0.0.1", 12000)
end

DCS.setUserCallbacks(test)