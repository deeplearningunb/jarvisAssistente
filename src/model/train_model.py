import pickle
import pandas as pd
from pydantic.dataclasses import dataclass
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential


@dataclass
class ModelTrain:
    data_path: str = "../data/commands.csv"

    def __post_init__(self) -> None:
        self.dataframe = pd.read_csv(self.data_path)
        self.dataframe = self.dataframe.sort_index()

    def __transform_x(self) -> None:
        self.vectorize = CountVectorizer()
        self.x = self.vectorize.fit_transform(
            self.dataframe["command"]
        ).toarray()

    def __transform_y(self) -> None:
        self.encoder = LabelEncoder()
        unique_labels = self.encoder.fit_transform(
            self.dataframe["label"].unique()
        )
        all_y = self.encoder.transform(self.dataframe["label"])
        self.hot_encoder = OneHotEncoder(sparse=False)
        _ = self.hot_encoder.fit(
            unique_labels.reshape(unique_labels.shape[0], 1)
        )
        self.y = self.hot_encoder.transform(all_y.reshape(all_y.shape[0], 1))

    def __create_model(self) -> None:
        input_dim = self.x.shape[1]
        self.model = Sequential()
        self.model.add(Dense(10, activation="relu", input_dim=input_dim))
        self.model.add(Dense(10, activation="sigmoid"))
        self.model.compile(optimizer='adam', loss="binary_crossentropy")

    def __train_model(self) -> None:
        self.__create_model()
        _ = self.model.fit(self.x, self.y, batch_size=2, epochs=200)

    def __model_save(self) -> None:
        self.model.save('./result.h5')
        with open('./encoders.pkl', 'wb') as f:
            encoder = {
                "encoder": self.encoder,
                "vectorize": self.vectorize
            }
            pickle.dump(encoder, f)

    def run(self) -> None:
        self.__transform_x()
        self.__transform_y()
        self.__train_model()
        self.__model_save()


if __name__ == "__main__":
    model = ModelTrain()
    model.run()
