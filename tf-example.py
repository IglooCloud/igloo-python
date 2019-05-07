from igloo import Client, User
import asyncio
import tensorflow as tf
mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)


async def main():
    client = Client(asyncio=True, token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VySWQiOiJmMTAyZGVhYy0wZGQyLTQwZWQtOTM4NS1lMzI3YjM0M2Y2ZmUiLCJ0b2tlbklkIjoiYWRjMjg4MzgtOGUyMi00OWYyLWI1ZDktYWI4M2Y0M2ZkN2RkIiwiYWNjZXNzTGV2ZWwiOiJERVZJQ0UiLCJ0b2tlblR5cGUiOiJQRVJNQU5FTlQifQ.f7GWid4sS8GhQB_qb9PQlI98ULp3HC3-63Ja97vuLYcFCzg9vKF-P5b1GBCgh1t_2GD3qa2p_UeIF5y6Ues65g")

    async for data in client.subscription_root.deviceUpdated():
        print(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
