from datetime import datetime

import pandas as pd

import arez
import asyncio

DEV_ID = 0  # your Developer ID
AUTH_KEY = ""  # your Auth Key


async def get_champion(list, name):
    # for each champion in the list
    for i in range(0, len(list), 1):
        # if the champion name is equal to the champion name currently being played
        if list[i].champion.name == name:
            # return the champion object being player
            return list[i]


async def main():
    api = arez.PaladinsAPI(DEV_ID, AUTH_KEY)
    # days done: 10th-11th, 15h-16th, 17th-18th, 20th-21st, 23rd -24th
    matches = api.get_matches_for_queue(arez.Queue.Casual_Siege, start=datetime.fromisoformat('2021-04-25'), end=datetime.fromisoformat('2021-04-26'), language=None, reverse=False, local_time=True, expand_players=True)
    matchcolumns = ["id", "Map", "WinTeam", "duration"]
    matchdata = pd.DataFrame(columns=matchcolumns)
    matchdata.to_csv('match_data_temp.csv', mode='w', index=False)
    teamcolumns1 = ["id", "champ1", "champ2", "champ3", "champ4", "champ5", "cwinrate1", "cwinrate2", "cwinrate3",
                   "cwinrate4", "cwinrate5", "ckda1", "ckda2", "ckda3", "ckda4", "ckda5", "cdf1", "cdf2", "cdf3",
                   "cdf4", "cdf5", "alvl1", "alvl2", "alvl3", "alvl4", "alvl5", "awinrate1", "awinrate2", "awinrate3",
                   "awinrate4", "awinrate5", "kda1", "kda2", "kda3", "kda4", "kda5"]
    teamcolumns2 = ["id", "champ6", "champ7", "champ8", "champ9", "champ10", "cwinrate6", "cwinrate7", "cwinrate8",
                    "cwinrate9", "cwinrate10", "ckda6", "ckda7", "ckda8", "ckda9", "ckda10", "cdf6", "cdf7", "cdf8",
                    "cdf9", "cdf10", "alvl6", "alvl7", "alvl8", "alvl9", "alvl10", "awinrate6", "awinrate7",
                    "awinrate8", "awinrate9", "awinrate10", "kda6", "kda7", "kda8", "kda9", "kda10"]
    team1data = pd.DataFrame(columns=teamcolumns1)
    team1data.to_csv('team1_data_temp.csv', mode='w', index=False)
    team2data = pd.DataFrame(columns=teamcolumns2)
    team2data.to_csv('team2_data_temp.csv', mode='w', index=False)
    async for match in matches:
        try:
            # resets lists everytime
            champ1 = []
            cwinrate1 = []
            ckda1 = []
            cdf1 = []
            alvl1 = []
            awinrate1 = []
            akda1 = []
            champ2 = []
            cwinrate2 = []
            ckda2 = []
            cdf2 = []
            alvl2 = []
            awinrate2 = []
            akda2 = []
            # add match data to dataframe
            for i in range(5):
                # grabs every champion name
                champ1.append(match.team1[i].champion.name)
                # grabs champions statistics
                champions_stat = await get_champion(await match.team1[i].player.get_champion_stats(), match.team1[i].champion.name)
                cwinrate1.append(champions_stat.winrate)
                ckda1.append(champions_stat.kda2)
                cdf1.append(champions_stat.df)
                alvl1.append(match.team1[i].account_level)
                awinrate1.append(match.team1[i].player.casual.winrate)
                akda1.append(match.team1[i].kda2)

                # grabs every champion name
                champ2.append(match.team2[i].champion.name)
                # grabs champions statistics
                champions_stat = await get_champion(await match.team2[i].player.get_champion_stats(),
                                                    match.team2[i].champion.name)
                cwinrate2.append(champions_stat.winrate)
                ckda2.append(champions_stat.kda2)
                cdf2.append(champions_stat.df)
                alvl2.append(match.team2[i].account_level)
                awinrate2.append(match.team2[i].player.casual.winrate)
                akda2.append(match.team2[i].kda2)
            # add teams data to dataframe
            team1data.loc[0] = [match.id, champ1[0], champ1[1], champ1[2], champ1[3], champ1[4], cwinrate1[0],
                                cwinrate1[1], cwinrate1[2], cwinrate1[3], cwinrate1[4], ckda1[0], ckda1[1],
                                ckda1[2], ckda1[3], ckda1[4], cdf1[0], cdf1[1], cdf1[2], cdf1[3], cdf1[4], alvl1[0],
                                alvl1[1], alvl1[2], alvl1[3], alvl1[4], awinrate1[0], awinrate1[1], awinrate1[2],
                                awinrate1[3], awinrate1[4], akda1[0], akda1[1], akda1[2], akda1[3], akda1[4]]
            team2data.loc[0] = [match.id, champ2[0], champ2[1], champ2[2], champ2[3], champ2[4], cwinrate2[0],
                                cwinrate2[1], cwinrate2[2], cwinrate2[3], cwinrate2[4], ckda2[0], ckda2[1],
                                ckda2[2], ckda2[3], ckda2[4], cdf2[0], cdf2[1], cdf2[2], cdf2[3], cdf2[4], alvl2[0],
                                alvl2[1], alvl2[2], alvl2[3], alvl2[4], awinrate2[0], awinrate2[1], awinrate2[2],
                                awinrate2[3], awinrate2[4], akda2[0], akda2[1], akda2[2], akda2[3], akda2[4]]
            matchdata.loc[0] = [match.id, match.map_name, match.winning_team, match.duration]
            matchdata.to_csv('match_data_temp.csv', mode='a', header=False, index=False)
            team1data.to_csv('team1_data_temp.csv', mode='a', header=False, index=False)
            team2data.to_csv('team2_data_temp.csv', mode='a', header=False, index=False)
            print(matchdata, "                     ", team1data, "                      ", team2data)
            matchdata = pd.DataFrame(columns=matchcolumns)
            team1data = pd.DataFrame(columns=teamcolumns1)
            team2data = pd.DataFrame(columns=teamcolumns2)
        except Exception:
            pass
    await api.close()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())  # run the async loop
