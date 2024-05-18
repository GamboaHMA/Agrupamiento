import time
import matplotlib.pyplot as plt

#def cambiandoArgumento(dato):
#    for a in range(0, len(dato)):
#        dato[a] = dato[a] + 3

#dato = [2, 3]
#cambiandoArgumento(dato)
#print(dato)

#inicio = time.time()
#time.sleep(2)
#actual = time.time()
#result = actual - inicio
#print(f"Tiempo {result:.10f} segundos")

#for i in range(0, 3, 1):
#    print("asd")

x = [1,2,3,4,5,6,7,8,9,10,11]
y = [-0.8, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 0.3]

fig, ax = plt.subplots()
ax.barh(x, width = y)
plt.xlim(-1, 1)
plt.show()
print("a")