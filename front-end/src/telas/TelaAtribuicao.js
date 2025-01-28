import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  Pressable,
  StyleSheet,
  Image,
  Picker,
  Dimensions,
} from "react-native";
import Template from "../components/TemplatePrincipal";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import CustomModal from "../components/CustomModal";
import TransferList from "../components/TransferList";
import { useTheme } from "../context/ThemeContext";
import { BASE_URL } from "@env";

const TelaAtribuicao = () => {
  const navigation = useNavigation();
  const [pedido, setPedido] = useState("");
  const [selectedMotoboy, setSelectedMotoboy] = useState("");
  const [selectedPedido, setSelectedPedido] = useState("");
  const [motoboys, setMotoboys] = useState("");
  const [pedidos, setPedidos] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedPedidos, setSelectedPedidos] = useState([]);
  const [carregandoMotoboys, setCarregandoMotoboys] = useState(true);
  const [carregandoPedidos, setCarregandoPedidos] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode, toggleTheme } = useTheme();

  useEffect(() => {
    console.log(selectedMotoboy);
  });

  useEffect(() => {
    const updateLayout = () => {
      const width = Dimensions.get("window").width;
      setIsMobile(width < 768);
    };
    Dimensions.addEventListener("change", updateLayout);
    updateLayout();

    return () => {
      Dimensions.removeEventListener("change", updateLayout);
    };
  }, []);

  useEffect(() => {
    const carregarMotoboy = async () => {
      try {
        const response = await axios.get(BASE_URL + "/motoboy");

        setMotoboys(response.data);
        setCarregandoMotoboys(false);
      } catch (error) {
        console.log(error);
      }
    };

    const carregarPedidos = async () => {
      try {
        const response = await axios.get(BASE_URL + "/pedido");
        console.log(response.data);
        setPedidos(response.data);
        setCarregandoPedidos(false);
      } catch (error) {
        console.log(error);
      }
    };

    carregarMotoboy();
    carregarPedidos();
  }, []);

  const handleAtribuicao = async () => {
    console.log("entrei");
    for (let i = 0; i < selectedPedidos.length; i++) {
      try {
        const response = await axios.put(
          BASE_URL +
            "/pedido/" +
            selectedPedidos[i] +
            "/atribuir-motoboy/" +
            selectedMotoboy
        );
      } catch (error) {
        console.log("teste");
        setModalVisible(true);
        console.log(error);
      }

      setModalVisible(true);
    }
  };

  const handleCancelar = () => {
    setSelectedPedidos([]);
    setSelectedMotoboy("");
  };

  const buscarPedido = (pedidoId) => {
    const pedidoEncontrado = pedidos.find((pedido) => pedido.id == pedidoId);
    console.log("Pedido encontrado: " + pedidoEncontrado, pedidoId);
    return pedidoEncontrado;
  };

  const adicionarPedido = () => {
    setSelectedPedidos([...selectedPedidos, selectedPedido]);
    setSelectedPedido("");
  };

  const removerPedido = (index) => {
    const novosPedidos = [...selectedPedidos];
    novosPedidos.splice(index, 1);
    setSelectedPedidos(novosPedidos);
  };

  const styles = StyleSheet.create({
    image: {
      width: 80,
      height: 100,
    },
    textPedido: {
      fontWeight: "bold",
      color: "#B20000",
      textAlign: "center",
      fontFamily: "LuckiestGuy",
    },
    label: {
      fontSize: 16,
      fontWeight: "bold",
      marginBottom: 8,
      color: isDarkMode ? "#000" : "#fff",
    },
    input: {
      height: 40,
      backgroundColor: isDarkMode ? "#fff" : "#434141",
      borderColor: isDarkMode ? "#ccc" : "#434141",
      borderWidth: 1,
      borderRadius: 4,
      marginBottom: 16,
      paddingHorizontal: 5,
      width: "80%",
    },
    button: {
      backgroundColor: "#015500",
      borderRadius: 10,
      paddingVertical: 15,
      paddingHorizontal: 15,
      alignItems: "center",
    },
    buttonText: {
      color: "white",
      fontSize: 16,
      fontWeight: "bold",
    },
    posicaoImage: {
      marginLeft: 20,
    },
    menuSuperior: {
      flexDirection: "row",
      justifyContent: "center",
      alignItems: "center",
      marginTop: 20,
    },

    tituloContainer: {
      flexDirection: "row",
      alignItems: "center",
      justifyContent: "center",
      marginBottom: 20,
    },
  });

  return (
    <Template imagem={"../../assets/images/bg-opaco.png"}>
      <CustomModal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        modalText="Pedido(s) atribuído(s) com sucesso"
      />
      <View style={[styles.containerSecundario, { margin: 30 }]}>
        <View style={styles.tituloContainer}>
          <Text
            style={[
              styles.textPedido,
              { fontSize: isMobile ? 30 : 60, marginTop: 30 },
            ]}
          >
            Atribuição de Pedidos
          </Text>
        </View>

        <View style={{ flexDirection: "row" }}>
          <View style={{ flex: 2, flexDirection: "column" }}>
            <View>
              <Text style={styles.label}>Motoboy</Text>
              <Picker
                selectedValue={selectedMotoboy}
                onValueChange={(itemValue) => setSelectedMotoboy(itemValue)}
                testID="motoboy-picker"
                style={[
                  styles.input,
                  {
                    color: isDarkMode ? "#000" : "#fff",
                    backgroundColor: isDarkMode ? "#fff" : "#434141",
                  },
                ]}
              >
                <Picker.Item label="Selecione um motoboy" value="" />
                {!carregandoMotoboys &&
                  motoboys.map((motoboy) => (
                    <Picker.Item
                      key={motoboy.id}
                      label={motoboy.nome}
                      value={motoboy.id}
                      color={isDarkMode ? "#000" : "#fff"}
                    />
                  ))}
              </Picker>
            </View>

            <View>
              <Text style={styles.label}>Pedido</Text>
              {!carregandoPedidos && (
                <TransferList
                  pedidos={pedidos}
                  setSelectedPedidos={setSelectedPedidos}
                />
              )}
            </View>

            <View style={{ flexDirection: "row", marginTop: 20 }}>
              <Pressable
                style={[styles.button, { marginRight: 10 }]}
                onPress={handleAtribuicao}
                testID="atribuir-btn"
              >
                <Text style={styles.buttonText}>Atribuir</Text>
              </Pressable>
              <Pressable
                style={[styles.button, { backgroundColor: "#B20000" }]}
                onPress={handleCancelar}
                testID="cancelar-btn"
              >
                <Text style={styles.buttonText}>Cancelar</Text>
              </Pressable>
            </View>
          </View>
          {!isMobile && (
            <View style={{ flex: 1 }}>
              <Image
                source={require("../../assets/images/logo.png")}
                style={[styles.image, { width: 440, height: 440 }]}
                resizeMode="contain"
              />
            </View>
          )}
        </View>
      </View>
    </Template>
  );
};

export default TelaAtribuicao;
