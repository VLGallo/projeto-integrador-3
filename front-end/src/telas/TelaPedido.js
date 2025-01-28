import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  Image,
  Picker,
  Dimensions,
} from "react-native";
import Template from "../components/TemplatePrincipal";
import { useNavigation } from "@react-navigation/native";
import axios from "axios";
import { useTheme } from "../context/ThemeContext";
import {
  FormControlLabel,
  Checkbox,
  Grid,
  Typography,
  IconButton,
} from "@mui/material";
import CustomModal from "../components/CustomModal";
import TransferListProduto from "../components/TransferListProduto";
import { BASE_URL } from "@env";

const TelaPedido = () => {
  const [clientes, setClientes] = useState("");
  const [modalVisible, setModalVisible] = useState(false);
  const [clienteSelecionado, setClienteSelecionado] = useState("");
  const [carregandoClientes, setCarregandoClientes] = useState(true);
  const [itens, setItens] = useState([]);
  const [carregandoProdutos, setCarregandoProdutos] = useState(true);
  const [produtos, setProdutos] = useState([]);
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode, toggleTheme } = useTheme();

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
    const carregarCliente = async () => {
      try {
        const response = await axios.get(BASE_URL + "/cliente");
        setClientes(response.data);
        setCarregandoClientes(false);
      } catch (error) {
        console.log(error);
      }
    };

    carregarCliente();
  }, []);

  const handleSalvar = async () => {
    const clienteSelecionadoObj = clientes.find(
      (cliente) => cliente.id == clienteSelecionado
    );
    console.log(clienteSelecionadoObj);
    console.log(itens);

    const produtosIds = itens.map((item) => item.id);
    console.log(produtosIds);

    try {
      const response = await axios.post(BASE_URL + "/pedido/add", {
        produtos: produtosIds,
        cliente: clienteSelecionado,
        funcionario: 1,
      });

      if (response.status >= 200 && response.status < 400) {
        setModalVisible(true);
        setItens([]);
        setClienteSelecionado("");
        setSelectedProduct("");
      }
    } catch (error) {
      setModalVisible(true);
      console.log(error);
    }
  };

  const carregarProdutos = async () => {
    try {
      const response = await fetch(BASE_URL + "/produto");
      const data = await response.json();
      setProdutos(data);
    } catch (error) {
      console.error("Erro ao carregar produtos:", error);
    } finally {
      setCarregandoProdutos(false); // Mover para o final da função
    }
  };

  useEffect(() => {
    setCarregandoProdutos(true); // Inicia o carregamento
    carregarProdutos();
  }, []);

  const handleCancelar = () => {
    setClienteSelecionado([]);
    setItens([]);
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
      borderColor: isDarkMode ? "#ccc" : "#434141",
      backgroundColor: isDarkMode ? "#fff" : "#434141",
      borderWidth: 1,
      borderRadius: 4,
      marginBottom: 16,
      paddingHorizontal: 5,
      width: "100%",
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
        modalText="Pedido cadastrado com sucesso"
      />
      <View>
        <View style={styles.tituloContainer}>
          <Text style={[styles.textPedido, { fontSize: isMobile ? 30 : 60 }]}>
            Pedidos
          </Text>
        </View>

        <View style={{ flexDirection: "row" }}>
          <View style={{ flex: 2, flexDirection: "column", padding: 30 }}>
            <View>
              <Text style={styles.label}>Cliente</Text>
              <Picker
                selectedValue={clienteSelecionado}
                onValueChange={(itemValue) => setClienteSelecionado(itemValue)}
                testID="cliente-picker"
                style={[
                  styles.input,
                  {
                    color: isDarkMode ? "#000" : "#fff",
                    backgroundColor: isDarkMode ? "#fff" : "#434141",
                  },
                ]}
              >
                <Picker.Item
                  label="Selecione um cliente"
                  value=""
                />
                {!carregandoClientes &&
                  clientes.map((cliente) => (
                    <Picker.Item
                      key={cliente.id}
                      label={cliente.nome}
                      value={cliente.id}
                      color={isDarkMode ? "#000" : "#fff"}
                    />
                  ))}
              </Picker>
            </View>

            <View style={{ marginTop: 20 }}>
              <Grid container direction="column" spacing={0}>
                <Typography
                  style={{
                    fontWeight: "bold",
                    color: isDarkMode ? "#000" : "#fff",
                  }}
                >
                  Itens
                </Typography>

                <View>
                  {!carregandoProdutos && (
                    <TransferListProduto
                      produtos={produtos}
                      setSelectedProdutos={setItens}
                    />
                  )}
                </View>
              </Grid>
            </View>

            <View style={{ flexDirection: "row", marginTop: 20 }}>
              <Pressable
                style={[styles.button, { marginRight: 10 }]}
                onPress={handleSalvar}
                testID="salvar-btn"
              >
                <Text style={styles.buttonText}>Salvar</Text>
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

          {/* Oculta a imagem em dispositivos móveis */}
          {!isMobile && (
            <View style={{ flex: 1, flexDirection: "column" }}>
              <Image
                source={require("../../assets/images/logo.png")}
                style={[styles.image, { width: 400, height: 400 }]}
                resizeMode="contain"
              />
            </View>
          )}
        </View>
      </View>
    </Template>
  );
};

export default TelaPedido;
