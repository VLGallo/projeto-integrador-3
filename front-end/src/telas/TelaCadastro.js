import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  Image,
  Dimensions,
} from "react-native";
import Template from "../components/TemplatePrincipal";
import CustomModal from "../components/CustomModal";
import axios from "axios";
import { useTheme } from "../context/ThemeContext";
import { BASE_URL } from '@env';

const TelaCadastro = () => {
  // const [modalVisible, setModalVisible] = useState("");
  const [modalVisible, setModalVisible] = useState(false);
  const [erroModalVisible, setErroModalVisible] = useState(false);
  const [mensagemErro, setMensagemErro] = useState("");
  const [nome, setNome] = useState("");
  const [telefone, setTelefone] = useState("");
  const [placa, setPlaca] = useState("");
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
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

  const handleSalvar = async () => {
    if (!nome) {
      setMensagemErro("O campo Nome é obrigatório.");
      setErroModalVisible(true);
      return;
    }
    
    
    if (telefone.length < 10 || telefone.length > 11) {
      setMensagemErro("O telefone deve conter 10 ou 11 dígitos.");
      setErroModalVisible(true);
      return;
    }
    
    if (placa.length !== 7) {
      setMensagemErro("A placa deve conter exatamente 7 caracteres.");
      setErroModalVisible(true);
      return;
    }    
    if (!usuario) {
      setMensagemErro("O campo Usuário é obrigatório.");
      setErroModalVisible(true);
      return;
    }

    if (!senha) {
      setMensagemErro("O campo Senha é obrigatório.");
      setErroModalVisible(true);
      return;
    }
    
    try {
      const response = await axios.post(BASE_URL + "/motoboy/add", {
        nome: nome,
        telefone: telefone,
        placa: placa,
        funcionario: 1,
        usuario: usuario,
        senha: senha,
      });
      console.log(response);
  
      if (response.status === 201) {
        setModalVisible(true);
        setNome("");
        setTelefone("");
        setPlaca("");
        setUsuario("");
        setSenha("");
      }
    } catch (error) {
      let mensagem = "Erro ao cadastrar motoboy.";
    
      if (error.response?.data?.detail) {
        const detailString = error.response.data.detail;
    
        // Regex para pegar a mensagem dentro de string=''
        const match = detailString.match(/string='(.+?)'/);
        if (match && match[1]) {
          mensagem = match[1];
        }
      }
    
      // Tornar mensagem mais amigável
      if (mensagem.toLowerCase().includes("usuario já existe")) {
        mensagem = "Esse nome de usuário já está em uso. Tente outro.";
      } else if (mensagem.toLowerCase().includes("motoboy com este usuario já existe")) {
        mensagem = "Já existe um motoboy com esse usuário.";
      } else if (mensagem.toLowerCase().includes("placa já existe")) {
        mensagem = "Essa placa já está cadastrada.";
      }
    
      console.log("Erro completo:", error.response);
      setMensagemErro(mensagem);
      setErroModalVisible(true);
    }
  };
  
  const handleCancelar = () => {
    setNome("");
    setTelefone("");
    setPlaca("");
    setUsuario("");
    setSenha("");
  };

  const styles = StyleSheet.create({
    label: {
      fontSize: 16,
      fontWeight: "bold",
      marginBottom: 8,
      color: isDarkMode ? "#000" : "#fff",
    },
    input: {
      height: 40,
      width: 150,
      borderColor: isDarkMode ? "#ccc" : "#434141",
      color: isDarkMode ? "#000" : "#fff",
      borderWidth: 1,
      borderRadius: 4,
      marginBottom: 16,
      paddingHorizontal: 5,
      backgroundColor: isDarkMode ? "#fff" : "#434141",
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
    tituloContainer: {
      flexDirection: "row",
      alignItems: "center",
      justifyContent: isMobile ? "center" : "flex-start",
      marginBottom: 40,
    },
    textEntregadores: {
      fontFamily: "LuckiestGuy",
      color: "rgb(178, 0, 0)",
      fontWeight: "bold",
      textAlign: isMobile ? "center" : "left",
    },
  });

  return (
    <Template imagem={"../../assets/images/bg-opaco.png"}>
      <CustomModal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        modalText="Entregador(a) cadastrado(a) com sucesso"
      />

      <CustomModal
        modalVisible={erroModalVisible}
        setModalVisible={setErroModalVisible}
        modalText={mensagemErro}
      />

      <View style={styles.tituloContainer}>
        <Text style={[styles.textEntregadores, {  fontSize: isMobile ? 40 : 60}]}>
          Cadastro de Entregadores
        </Text>
      </View>

      <View style={{ flexDirection: "row" }}>
        <View style={{ flex: 3 }}>
          <View>
            <Text style={styles.label}> Nome</Text>
            <TextInput
              style={styles.input}
              value={nome}
              onChangeText={setNome}
              testID="nome-entregador-input"
            />
          </View>
          <View>
            <Text style={styles.label}>Telefone</Text>
            <TextInput
              style={styles.input}
              value={telefone}
              onChangeText={setTelefone}
              testID="telefone-entregador-input"
            />
          </View>
          <View>
            <Text style={styles.label}>Placa</Text>
            <TextInput
              style={styles.input}
              value={placa}
              onChangeText={setPlaca}
              testID="placa-entregador-input"
            />
          </View>
          <View>
            <Text style={styles.label}>Usuário</Text>
            <TextInput
              style={styles.input}
              value={usuario}
              onChangeText={setUsuario}
              testID="usuario-entregador-input"
            />
          </View>
          <View>
            <Text style={styles.label}>Senha</Text>
            <TextInput
              style={styles.input}
              value={senha}
              onChangeText={setSenha}
              secureTextEntry={true}
              testID="senha-entregador-input"
            />
          </View>
          <View style={{ flexDirection: "row" }}>
            <Pressable
              style={[styles.button, { marginRight: 10 }]}
              onPress={handleSalvar}
              testID="salvar-entregador-btn"
            >
              <Text style={styles.buttonText}>Salvar</Text>
            </Pressable>
            <Pressable
              style={[styles.button, { backgroundColor: "#B20000" }]}
              onPress={handleCancelar}
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

export default TelaCadastro;
