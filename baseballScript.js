// global variables
var leagueLeaders;

// helper functions
function dataToHTML(map, year, type) {
	const GP = map.get("gamesPlayed");
	const PA = map.get("plateAppearances");
	const AB = map.get("atBats");
	const BB = map.get("baseOnBalls");
	const Hits = map.get("hits");
	const Doubles = map.get("doubles");
	const Triples = map.get("triples");
	const HR = map.get("homeRuns");
	const AVG = map.get("avg");
	const OBP = map.get("obp");
	const SLG = map.get("slg");
	const OPS = map.get("ops");
	const RBI = map.get("rbi");
	const Runs = map.get("runs");
	const SO = map.get("strikeOuts");
	const SB = map.get("stolenBases");
	const BABIP = map.get("babip");
	const HBP = map.get("hitByPitch");
	let htmlDataStr = ``;
	if (type == 'single') {
		htmlDataStr += `<tr> `;
	}
	//const htmlDataStr = ("<tr> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> </tr>", GP, PA, AB, BB, Hits, Doubles, Triples, HR, AVG, OBP, SLG, OPS, RBI, Runs, SO, SB, BABIP, HBP);
	htmlDataStr += `<td> ${year} </td> <td> ${GP} </td> <td> ${PA} </td> <td> ${AB} </td> <td> ${BB} </td> <td> ${Hits} </td> <td> ${Doubles} </td> <td> ${Triples} </td> <td> ${HR} </td> <td> ${AVG} </td> <td> ${OBP} </td> <td> ${SLG} </td> <td> ${OPS} </td> <td> ${RBI} </td> <td> ${Runs} </td> <td> ${SO} </td> <td> ${SB} </td> <td> ${BABIP} </td> <td> ${HBP} </td> </tr>`;
	return htmlDataStr;	
}
function pitcherDataToHTML(map, year, type) {
	const starts = map.get("gamesStarted")
	const GP = map.get("gamesPlayed");
	const IP = map.get("inningsPitched");
	const W = map.get("wins");
	const L = map.get("losses");
	const ERA = map.get("era");
	const oppAvg = map.get("avg");
	const whip = map.get("whip");
	const SO = map.get("strikeOuts");
	const BB = map.get("baseOnBalls");
	const hits = map.get("hits");
	const HR = map.get("homeRuns");
	const strikeP = map.get("strikePercentage");
	const saves = map.get("saves");
	const saveOpps = map.get("saveOpportunities");
	const CG = map.get("completeGames");
	const shutOuts = map.get("shutouts");
	const wildPitches = map.get("wildPitches");
	let htmlDataStr = ``;
	if (type == 'single') {
		htmlDataStr += `<tr> `;
	}
	htmlDataStr += `<td> ${year} </td> <td> ${starts} </td> <td> ${GP} </td> <td> ${IP} </td> <td> ${W} </td> <td> ${L} </td> <td> ${ERA} </td> <td> ${oppAvg} </td> <td> ${whip} </td> <td> ${SO} </td> <td> ${BB} </td> <td> ${hits} </td> <td> ${HR} </td> <td> ${strikeP} </td> <td> ${saves} </td> <td> ${saveOpps} </td> <td> ${CG} </td> <td> ${shutOuts} </td> <td> ${wildPitches} </td> </tr>`;
	return htmlDataStr;	
}
function playerInfoToHTML(player_data) {
	const name = player_data[4] + " " + player_data[6];
	const position = player_data[2];
	const number = player_data[0];
	const htmlDataStr = `<tr> <td> ${name} </td> <td> ${position} </td> <td> ${number} </td>`;
	return htmlDataStr;
}
function leaderDataToHTML(data) {
	const rank = data[0][0];
	const name = data[0][1];
	const team = data[0][2];
	const value = data[0][3];
	const htmlDataStr = `<tr> <td> ${rank} </td> <td> ${name} </td> <td> ${team} </td> <td> ${value} </td> </tr>`;
	return htmlDataStr;
}
function standingsToHTML(team) {
	const rank = team.get('div_rank');
	const name = team.get('name');
	const w = team.get('w');
	const l = team.get('l');
	const gb = team.get('gb');
	const wc_rank = team.get('wc_rank');
	const wc_gb = team.get('wc_gb');
	const htmlDataStr = `<tr> <td> ${rank} </td> <td> ${name} </td> <td> ${w} </td> <td> ${l} </td> <td> ${gb} </td> <td> ${wc_rank} </td> <td> ${wc_gb} </td> </tr>`;
	return htmlDataStr;
}
function teamLeadersToHTML(map) {
	let htmlDataStr = `<tr> `;
	for (const key of map.keys()){
		let statLeaders = map.get(key);
		let rank1 = statLeaders[0];
		let name = rank1[1];
		let value = rank1[2];
		htmlDataStr += `<td> ${name} :  ${value} </td>`;
	}
	htmlDataStr += ` <tr>`;
	return htmlDataStr;
}
function rankToMap(leadersData, player, playerRanks, stat) {
	for (let i = 0; i < leadersData.length; i++) {
		if (player == leadersData[i][1]) {
			let rank = leadersData[i][0];
			let data = [rank, leadersData.length];
			playerRanks.set(stat, data);
			break;
		}
	}
}
function checkPitcherRank(player) {
	let playerRanks = new Map();
	for (const key of leagueLeaders.keys()) {
		let leadersData = leagueLeaders.get(key);
		if (key == "ERA") {
			rankToMap(leadersData, player, playerRanks, "ERA");
		} else if (key == "WHIP") {
			rankToMap(leadersData, player, playerRanks, "WHIP");
		} else if (key == "SO") {
			rankToMap(leadersData, player, playerRanks, "SO");
		} else if (key == "IP") {
			rankToMap(leadersData, player, playerRanks, "IP");
		}
	}
	return playerRanks;
}
function checkPositionPlayerRank(player) {
	let playerRanks = new Map();
	for (const key of leagueLeaders.keys()) {
		let leadersData = leagueLeaders.get(key);
		if (key == "BA") {
			rankToMap(leadersData, player, playerRanks, "BA");
		} else if (key == "OBP") {
			rankToMap(leadersData, player, playerRanks, "OBP");
		} else if (key == "SLG") {
			rankToMap(leadersData, player, playerRanks, "SLG");
		} else if (key == "OPS") {
			rankToMap(leadersData, player, playerRanks, "OPS");
		} else if (key == "Hits") {
			rankToMap(leadersData, player, playerRanks, "Hits");
		} else if (key == "HR") {
			rankToMap(leadersData, player, playerRanks, "HR");
		} else if (key == "SB") {
			rankToMap(leadersData, player, playerRanks, "SB");
		} else if (key == "RBI") {
			rankToMap(leadersData, player, playerRanks, "RBI");
		}
	}
	return playerRanks;
}
function ranksToString(playerRankMap, player) {
	if (playerRankMap.size == 0) {
		return player + " is not qualified to be ranked in any statistic";
	} 
	let rankStr = player + " is ranked: ";
	const keys = Array.from(playerRankMap.keys());
	for (let i = 0; i < keys.length - 1; i++) {
		let data = playerRankMap.get(keys[i]);
		let rank = data[0];
		let total = data[1];
		if (rank <= 10) {
			rankStr += "<b>" + rank + " out of " + total + " in " + keys[i] + "</b>, ";
		} else {
			rankStr += rank + " out of " + total + " in " + keys[i] + ", ";
		}
	}
	let lastStat = keys[keys.length - 1];
	let lastData = playerRankMap.get(lastStat);
	let lastRank = lastData[0];
	let lastTotal = lastData[1];
	if (lastRank <= 10) {
		rankStr += "<b>" + lastRank + " out of " + lastTotal + " in " + lastStat + "</b>";
	} else {
		rankStr += lastRank + " out of " + lastTotal + " in " + lastStat;
	}
	return rankStr;
}

// functions called when user presses button
function getData(player_type) {
	$("#statsTable").find("tr:gt(0)").remove();
	$("#pitcherStatsTable").find("tr:gt(0)").remove();
	if (player_type == "hitting") {
		var playerNameInput = document.getElementById("player_name").value;
		var playerRanks = checkPositionPlayerRank(playerNameInput);
		document.getElementById("playerRanks").innerHTML = ranksToString(playerRanks, playerNameInput);
	} else {
		var playerNameInput = document.getElementById("pitcher_name").value;
		var playerRanks = checkPitcherRank(playerNameInput);
		document.getElementById("playerRanks").innerHTML = ranksToString(playerRanks, playerNameInput);
	}
	$.ajax({
		type: 'get',
		url: 'http://127.0.0.1:5000/career',
		data: {'player_name':playerNameInput, 'player_type':player_type},
		dataType: 'json',
		success: function (data) {
			const data2 = JSON.stringify(data);
			const map = new Map(Object.entries(JSON.parse(data2)));
			
			if (player_type == "hitting") {
				statsTable = document.getElementById('statsTable');
				statsTable.innerHTML += dataToHTML(map, 'Career', 'single');
			} else {
				statsTable = document.getElementById('pitcherStatsTable');
				statsTable.innerHTML += pitcherDataToHTML(map, 'Career', 'single');
			}
			
			document.getElementById("getDataResponse").innerHTML = "Success, found player!"
		},
		error: function (error) {
			document.getElementById("getDataResponse").innerHTML = "Error player not found, player may be inactive or you misspelled the name"
			console.log(`Error ${error}`);
		}
	});
	$.ajax({
		type: 'get',
		url: 'http://127.0.0.1:5000/seasons',
		data: {'player_name':playerNameInput, 'player_type':player_type},
		dataType: 'json',
		success: function (data) {
			const data2 = JSON.stringify(data);
			const map = new Map(Object.entries(JSON.parse(data2)));
			
			if (player_type == "hitting") {
				statsTable = document.getElementById('statsTable');
			} else {
				statsTable = document.getElementById('pitcherStatsTable');
			}

			for (const key of map.keys()){
				var value = new Map(Object.entries(map.get(key)));
				if (player_type == "hitting") {
					statsTable.innerHTML += dataToHTML(value, key, 'single');
				} else {
					statsTable.innerHTML += pitcherDataToHTML(value, key, 'single');
				}
			}
		},
		error: function (error) {
			console.log(`Error ${error}`);
		}
	});
}
function getLeagueLeaders() {
    $.ajax({
        type: 'get',
        url: 'http://127.0.0.1:5000/leaders',
        success: function (data) {
            const data2 = JSON.stringify(data);
            leagueLeaders = new Map(Object.entries(JSON.parse(data2)));

            for (const key of leagueLeaders.keys()){
                var value = leagueLeaders.get(key);
                if (key == "ERA") {
                    document.getElementById("eraLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "WHIP") {
                    document.getElementById("whipLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "SO") {
                    document.getElementById("soLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "IP") {
                    document.getElementById("ipLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "BA") {
                    document.getElementById("avgLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "OBP") {
                    document.getElementById("obpLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "SLG") {
                    document.getElementById("slgLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "OPS") {
                    document.getElementById("opsLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "Hits") {
                    document.getElementById("hitsLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "HR") {
                    document.getElementById("hrLeader").innerHTML += leaderDataToHTML(value);
                } else if (key == "SB") {
                    document.getElementById("sbLeader").innerHTML += leaderDataToHTML(value);
                } else { // RBI
                    document.getElementById("rbiLeader").innerHTML += leaderDataToHTML(value);
                } 
            }
            },
        error: function (error) {
            console.log(`Error ${error}`);
        }
    });
}
function getTeamData() {
	$("#hittersTable").find("tr:gt(0)").remove();
	$("#pitchersTable").find("tr:gt(0)").remove();
	let teamNameInput = document.getElementById("team_name").value;
	$.ajax({
		type: 'get',
		url: 'http://127.0.0.1:5000/roster',
		data: {'team_name':teamNameInput},
		dataType: 'json',
		success: function (data) {
			const data2 = JSON.stringify(data);
			const map = new Map(Object.entries(JSON.parse(data2)));

			let hittersTable = document.getElementById('hittersTable');
			let pitchersTable = document.getElementById('pitchersTable');

			for (const key of map.keys()){
				let value = new Map(Object.entries(map.get(key)));
				let player_data = key.split(/(\s+)/);
				let player_info_html = playerInfoToHTML(player_data); 
				if (player_data[2] == "P") {
					let player_stats_html = pitcherDataToHTML(value, value.get("year"), 'roster');
					let player_total_info = player_info_html + player_stats_html;
					pitchersTable.innerHTML += player_total_info;
				} else {
					let player_stats_html = dataToHTML(value, value.get("year"), 'roster');
					let player_total_info = player_info_html + player_stats_html;
					hittersTable.innerHTML += player_total_info;
				}
				
			}
		},
		error: function (error) {
			console.log(`Error ${error}`);
		}
	});
}
function getDivisionStandings() {
	$("#divisionTable").find("tr:gt(0)").remove();
	let teamNameInput = document.getElementById("team_name").value;
	$.ajax({
		type: 'get',
		url: 'http://127.0.0.1:5000/teamStandings',
		data: {'team_name':teamNameInput},
		dataType: 'json',
		success: function (data) {
			const data2 = JSON.stringify(data);
			const map = new Map(Object.entries(JSON.parse(data2)));

			let divisionTable = document.getElementById('divisionTable');

			let divName = map.get('div_name');
			let teams = map.get('teams');
			
			document.getElementById('divName').innerHTML = divName;
			for (let i = 0; i < teams.length; i++) {
				let team = teams[i];
				team = new Map(Object.entries(team));
				if (team.get('name') == teamNameInput) {
					let teamW = team.get('w');
					let teamL = team.get('l');
					let teamRecordStr = "Record: " + teamW + "-" + teamL;
					let teamRankStr = "Rank " + team.get('div_rank') + " in the " + divName;
					document.getElementById('teamRecord').innerHTML = teamRecordStr;
					document.getElementById('teamRank').innerHTML = teamRankStr;
				}
				divisionTable.innerHTML += standingsToHTML(team);
			}
		},
		error: function (error) {
			console.log(`Error ${error}`);
		}
	});
}
function getTeamLeaders() {
	$("#leadersTable").find("tr:gt(0)").remove();
	let teamNameInput = document.getElementById("team_name").value;
	$.ajax({
		type: 'get',
		url: 'http://127.0.0.1:5000/teamLeaders',
		data: {'team_name':teamNameInput},
		dataType: 'json',
		success: function (data) {
			const data2 = JSON.stringify(data);
			const map = new Map(Object.entries(JSON.parse(data2)));
			
			document.getElementById('leadersTable').innerHTML += teamLeadersToHTML(map);
		},
		error: function (error) {
			console.log(`Error ${error}`);
		}
	});
}

