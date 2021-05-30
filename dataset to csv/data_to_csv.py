from datetime import datetime

import pandas as pd

import arez
import asyncio

DEV_ID = 0  # your Developer ID
AUTH_KEY = ""  # your Auth Key

async def main():
    async with arez.PaladinsAPI(DEV_ID, AUTH_KEY) as api:
        matches = api.get_matches_for_queue(arez.Queue.Casual_Siege, start=datetime.fromisoformat('2021-05-16'),
                                            end=datetime.fromisoformat('2021-05-17'), language=None, reverse=False,
                                            local_time=True, expand_players=True)
        teamcolumns1 = ["id", "WinTeam", "cwinrate1", "cwinrate2", "cwinrate3", "cwinrate4", "cwinrate5", "ckda1", "ckda2",
                        "ckda3", "ckda4", "ckda5", "cdf1", "cdf2", "cdf3", "cdf4", "cdf5", "cwinrate6", "cwinrate7",
                        "cwinrate8", "cwinrate9", "cwinrate10", "ckda6", "ckda7", "ckda8", "ckda9", "ckda10", "cdf6",
                        "cdf7", "cdf8", "cdf9", "cdf10", "cwinratedif", "ckdadif", "cdfdif"]
        team1data = pd.DataFrame(columns=teamcolumns1)
        team1data.to_csv('data_temp.csv', mode='w', index=False)
        async for match in matches:
            try:
                # resets lists everytime
                cwinrate1 = []
                ckda1 = []
                cdf1 = []
                cwinrate2 = []
                ckda2 = []
                cdf2 = []
                # add match data to dataframe
                for i in range(5):
                    # grabs champions statistics
                    champions_stat = arez.utils.get(await match.team1[i].player.get_champion_stats(),
                                                    champion__name=match.team1[i].champion.name)
                    cwinrate1.append(champions_stat.winrate)
                    ckda1.append(champions_stat.kda2)
                    cdf1.append(champions_stat.df)

                    # grabs champions statistics
                    champions_stat = arez.utils.get(await match.team2[i].player.get_champion_stats(),
                                                    champion__name=match.team2[i].champion.name)
                    cwinrate2.append(champions_stat.winrate)
                    ckda2.append(champions_stat.kda2)
                    cdf2.append(champions_stat.df)
                sum1 = 0
                sum2 = 0
                sum3 = 0
                sum4 = 0
                sum5 = 0
                sum6 = 0
                for i in range(5):
                    sum1 += cwinrate1[i]
                    sum2 += ckda1[i]
                    sum3 += cdf1[i]
                    sum4 += cwinrate2[i]
                    sum5 += ckda2[i]
                    sum6 += cdf2[i]
                cwinratedif = sum1/5 - sum4/5
                ckdadif = sum2/5 - sum5/5
                cdfdif = sum3/5 - sum6/5
                # add teams data to dataframe
                team1data.loc[0] = [match.id, match.winning_team - 1, cwinrate1[0], cwinrate1[1], cwinrate1[2],
                                    cwinrate1[3], cwinrate1[4], ckda1[0], ckda1[1], ckda1[2], ckda1[3], ckda1[4], cdf1[0],
                                    cdf1[1], cdf1[2], cdf1[3], cdf1[4], cwinrate2[0], cwinrate2[1], cwinrate2[2],
                                    cwinrate2[3], cwinrate2[4], ckda2[0], ckda2[1], ckda2[2], ckda2[3], ckda2[4], cdf2[0],
                                    cdf2[1], cdf2[2], cdf2[3], cdf2[4], cwinratedif, ckdadif, cdfdif]
                print(team1data)
                team1data.to_csv('data_temp.csv', mode='a', header=False, index=False)
                team1data = pd.DataFrame(columns=teamcolumns1)
            except Exception:
                pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())  # run the async loop
