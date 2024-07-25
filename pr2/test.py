import playlist
import pickle

pl1 = playlist.PlayList("1")
pl1.append(playlist.Composition("""C:/Users/yormu/Music/PMUSIC.mp3"""))
pl1.append(playlist.Composition("C:/Users/yormu/Music/Rick_Astley_-_Never_Gonna_Give_You_Up_48032892.mp3"))
pl2 = playlist.PlayList("2")
pl2.append(playlist.Composition("C:/Users/yormu/Music/PMUSIC.mp3"))
pl2.append(playlist.Composition("C:/Users/yormu/Music/Scatman_John_-_Scatman_48230333.mp3"))
data = [pl1, pl2]
with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)
