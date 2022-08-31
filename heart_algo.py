def algorytm(sciezka):
    import wfdb
    import math
    import matplotlib.pyplot as plt
    from statistics import mean

    record = wfdb.rdrecord(sciezka)  # wartości plików numer próbki w której występuje pik
    wartosci = wfdb.rdann(sciezka, 'atr').sample
    ECG1 = record.p_signal[:, 0]  # odprowadzenie I
    ECG6 = record.p_signal[:, 5]  # odprowadzenie aVF

    # --------------fragment liczacy srednią oś elektryczną z I i aVF -----------------
    meanaxis = []
    for i in range(len(wartosci)):
        if i > 30:  # 30 jest wpisane na oko by pozbyć się pików występujących w 0
            a = int(wartosci[i] - record.fs * 0.075)
            b = int(wartosci[i] + record.fs * 0.075)
            tabI = ECG1[a:b]
            tabaVF = ECG6[a:b]
            maxI = max(tabI)
            maxaVF = max(tabaVF)
            minI = min(tabI)
            minaVF = min(tabaVF)
            ampI = maxI - abs(minI)
            ampaVF = maxaVF - abs(minaVF)
            if ampI != 0 and ampaVF != 0:
                axis = math.atan((2 * ampaVF) / (math.sqrt(3) * ampI))
                axis = axis * (180 / math.pi)
                meanaxis.append(axis)


    # KONFIGURACJA PLOTÓW Z 2 ODPROWADZENIAMI SYGNAŁU EKG
    # -----------------------------------------------------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, constrained_layout=True)
    fig.suptitle('Wykres sygnałów ECG')
    ax1.plot(ECG1[:1000])
    ax1.set_title('I')
    ax2.plot(ECG6[:1000])
    ax2.set_title('AVF')

    return ECG1, ECG6, mean(meanaxis)