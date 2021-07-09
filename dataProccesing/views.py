from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import seaborn as sns
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class DataView(APIView):

    def cleanData(self, date):
        cred = credentials.Certificate('./cred.json')
        fire = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://testemg-wheeler-default-rtdb.firebaseio.com/'
        })
        ref = db.reference('GyroSensor/EMG')
        fire_result = ref.get()
        # from matplotlib import interactive
        print(fire_result.keys())
        emg_base = fire_result[date]
        print(type(emg_base))
        emg_base = emg_base.replace('[', '')
        emg_base = emg_base.replace(']', '')
        np_emg = np.fromstring(emg_base, dtype=float, sep=',')

        np_emg = np_emg / 3471.6

        plt.figure(1)
        x = np.linspace(0, 20, len(np_emg))
        plt.plot(x, np_emg, alpha=0.6, label='Rectified')
        plt.title('EMG signal rectified')
        plt.ylabel('mV')
        plt.xlabel('time[s]')
        # plt.show()
        print(np.max(np_emg))
        w_size = 20
        np_averages = np.array([])
        for i in range(0, len(np_emg) - w_size + 1):
            np_averages = np.append(np_averages, np_emg[i:i + w_size].mean())
        # print(len(np_averages))
        peaks, _ = find_peaks(np_averages, height=0.00005, distance=20)
        print(len(np_averages))
        x_av = np.linspace(0, 20, len(np_averages))
        plt.figure(1)
        plt.plot(x_av, np_averages, color='green', label='RMS')
        x_peaks = np.linspace(0, 20, len(peaks))
        # print(peaks)
        plt.plot(x_av[peaks], np_averages[peaks], 'X')
        # ************************************************************
        pd_emg = pd.Series(np_emg)
        pd_av = pd_emg.rolling(w_size, min_periods=1).mean()
        x_pd = np.linspace(0, 20, len(pd_av))
        print(pd_av)
        # plt.plot(x_pd, pd_av, label='pandas average', c='r', alpha=0.5)
        plt.legend()
        plt.savefig('./static/img/emg_average_{0}.png'.format(date))
        # interactive(True)
        # plt.show()

        frame = {'pandas_average': pd_av}
        emg_df = pd.DataFrame(frame)
        emg_df['np_averages'] = pd.Series(np_averages)
        emg_df = emg_df.fillna(method='pad')
        print(emg_df.head())
        print(emg_df.corr())
        print(emg_df.describe())
        plt.figure(2)
        emg_df.boxplot(column=['pandas_average', 'np_averages'])
        plt.savefig("./static/img/boxplot_{0}.png".format(date))
        # plt.scatter(emg_df.pandas_average, emg_df.np_averages)
        # plt.show()

        plt.figure(3)
        # plt.imshow(emg_df.corr(), cmap=plt.cm.Reds, interpolation='nearest')
        sns.heatmap(emg_df.corr())
        plt.savefig("./static/img/heatmap_{0}.png".format(date))
        firebase_admin.delete_app(fire)
        plt.close('all')

    def get(self, request,  *args, **kwargs):

        #print (kwargs)
        print()
        date = str(kwargs.get("month"))+'-'+str(kwargs.get("day"))+'-'+str(kwargs.get("year"))+'-'+str(kwargs.get("h"))+'-'+str(kwargs.get("m"))+'-'+str(kwargs.get("s"))
        self.cleanData(date)

        return Response(
            status=status.HTTP_201_CREATED,
            data = {"message": "successful"}
        )
        #