import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  Image,
  Alert,
  Dimensions,
} from "react-native";
import Template from "../components/TemplatePrincipal";
import CustomModal from "../components/CustomModal";
import axios from "axios";
import { useTheme } from "../context/ThemeContext";
import { BASE_URL } from "@env";

const TelaCliente = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [nome, setNome] = useState("");
  const [telefone, setTelefone] = useState("");
  const [cep, setCep] = useState("");
  const [logradouro, setLogradouro] = useState("");
  const [bairro, setBairro] = useState("");
  const [numero, setNumero] = useState("");
  const [complemento, setComplemento] = useState("");
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode, toggleTheme } = useTheme();

  const handleCadastrar = async () => {
    if (!isFormValid()) {
      Alert.alert("Atenção", "Todos os campos precisam ser preenchidos.");
      return;
    }

    try {
      const response = await axios.post(BASE_URL + "/cliente/add", {
        nome,
        telefone,
        cep,
        logradouro,
        bairro,
        numero,
        complemento,
      });

      if (response.status === 201) {
        setModalVisible(true);
        setNome("");
        setTelefone("");
        setCep("");
        setLogradouro("");
        setBairro("");
        setNumero("");
        setComplemento("");
      }
    } catch (error) {
      console.log(error);
    }
  };

  const handleCancelar = () => {
    setNome("");
    setTelefone("");
    setCep("");
    setLogradouro("");
    setBairro("");
    setNumero("");
    setComplemento("");
  };

  const isFormValid = () => {
    return nome && telefone && logradouro && bairro && numero;
  };

  const handleCepChange = async (newCep) => {
    setCep(newCep);

    // Verifica se o CEP tem 8 dígitos
    if (newCep.length === 8) {
      try {
        const response = await axios.get(
          `https://viacep.com.br/ws/${newCep}/json/`
        );
        const { logradouro, bairro, erro } = response.data;

        if (!erro) {
          setLogradouro(logradouro || "");
          setBairro(bairro || "");
        } else {
          Alert.alert("Erro", "CEP não encontrado.");
        }
      } catch (error) {
        console.log(error);
        Alert.alert("Erro", "Erro ao buscar o CEP.");
      }
    }
  };

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

  const styles = StyleSheet.create({
    label: {
      fontSize: 16,
      fontWeight: "bold",
      marginBottom: 8,
      color: isDarkMode ? "#000" : "#fff",
    },
    input: {
      height: 40,
      color: isDarkMode ? "#000" : "#fff",
      borderColor: isDarkMode ? "#ccc" : "#434141",
      borderWidth: 1,
      borderRadius: 4,
      marginBottom: 16,
      paddingHorizontal: 5,
      backgroundColor: isDarkMode ? "#fff" : "#434141",
      width: "98%",
    },
    smallInput: {
      height: 40,
      color: isDarkMode ? "#000" : "#fff",
      borderColor: isDarkMode ? "#ccc" : "#434141",
      borderWidth: 1,
      borderRadius: 4,
      paddingHorizontal: 2,
      backgroundColor: isDarkMode ? "#fff" : "#434141",
      width: "100%",
      marginBottom: 16,
    },
    row: {
      flexDirection: "row",
      justifyContent: "space-between",
    },
    smallInputContainer: {
      flex: 1,
      marginRight: 10,
    },
    button: {
      borderRadius: 10,
      paddingHorizontal: 15,
      paddingVertical: 15,
      alignItems: "center",
    },
    buttonText: {
      color: "#fff",
      textAlign: "center",
      fontSize: 16,
      fontWeight: "bold",
    },
    textCliente: {
      fontWeight: "bold",
      color: "#B20000",
      textAlign: "center",
      fontFamily: "LuckiestGuy",
    },
  });

  return (
    <Template imagem={"../../assets/images/bg-opaco.png"}>
      <CustomModal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        modalText="Cliente cadastrado com sucesso"
      />

      <View style={styles.tituloContainer}>
        <Text style={[styles.textCliente, { fontSize: isMobile ? 30 : 60 }]}>
          Cadastro de Clientes
        </Text>
      </View>

      <View style={{ flexDirection: "row" }}>
        <View style={{ flex: 3 }}>
          <View>
            <Text style={styles.label}>Nome</Text>
            <TextInput
              style={styles.input}
              value={nome}
              onChangeText={setNome}
              testID="nome-cliente-input"
            />
          </View>

          <View style={styles.row}>
            <View style={styles.smallInputContainer}>
              <Text style={styles.label}>Telefone</Text>
              <TextInput
                style={styles.smallInput}
                value={telefone}
                onChangeText={setTelefone}
                testID="telefone-input"
              />
            </View>
            <View style={styles.smallInputContainer}>
              <Text style={styles.label}>CEP</Text>
              <TextInput
                style={styles.smallInput}
                value={cep}
                onChangeText={handleCepChange}
                maxLength={8}
                keyboardType="numeric"
                testID="CEP-input"
              />
            </View>
          </View>

          <View>
            <Text style={styles.label}>Logradouro</Text>
            <TextInput
              style={styles.input}
              value={logradouro}
              onChangeText={setLogradouro}
              testID="logradouro-input"
            />
          </View>

          <View style={styles.row}>
            <View style={styles.smallInputContainer}>
              <Text style={styles.label}>Número</Text>
              <TextInput
                style={styles.smallInput}
                value={numero}
                onChangeText={setNumero}
                testID="numero-input"
              />
            </View>
            <View style={styles.smallInputContainer}>
              <Text style={styles.label}>Complemento</Text>
              <TextInput
                style={styles.smallInput}
                value={complemento}
                onChangeText={setComplemento}
                testID="complemento-input"
              />
            </View>
          </View>

          <View>
            <Text style={styles.label}>Bairro</Text>
            <TextInput
              style={styles.input}
              value={bairro}
              onChangeText={setBairro}
              testID="bairro-input"
            />
          </View>

          <View style={{ flexDirection: "row" }}>
            <Pressable
              style={[
                styles.button,
                {
                  backgroundColor: isFormValid() ? "#015500" : "#A9A9A9",
                  marginRight: 20,
                },
              ]}
              onPress={handleCadastrar}
              disabled={!isFormValid()}
              testID="cadastrar-btn"
            >
              <Text style={styles.buttonText}>Cadastrar</Text>
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
    </Template>
  );
};

export default TelaCliente;
