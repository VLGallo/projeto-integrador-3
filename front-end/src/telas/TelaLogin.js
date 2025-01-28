import {
  View,
  TextInput,
  StyleSheet,
  Text,
  Image,
  ImageBackground,
  Pressable,
  Dimensions,
  TouchableOpacity
} from "react-native";
import axios from "axios";
import React, { useState, useEffect } from "react";
import { useNavigation } from "@react-navigation/native";
import CustomModal from "../components/CustomModal";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { MaterialIcons } from '@expo/vector-icons'; 
import { useTheme } from "../context/ThemeContext";
import { BASE_URL } from '@env';

const TelaLogin = () => {
  const navigation = useNavigation();
  const [modalVisible, setModalVisible] = useState(false);
  const [usuario, setUsuario] = useState("");
  const [senha, setSenha] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode } = useTheme();
  const theme = isDarkMode ? "light" : "dark";

  const getCookie = async () => {
    const valorDoCookie = await AsyncStorage.getItem("usuario");
    return valorDoCookie;
  };

  const verificaLogado = async () => {
    try {
      const cookie = await getCookie("usuario");
      if (cookie) {
        navigation.navigate("TelaHome");
      }
    } catch (error) {
      console.error("Erro ao verificar se está logado:", error);
    }
  };

  useEffect(() => {
    verificaLogado();
  }, []); 

  const setCookie = async (usuario) => {
    try {
      await AsyncStorage.setItem("usuario", usuario);
      console.log("Cookie definido com sucesso");
    } catch (error) {
      console.error("Erro ao definir o cookie:", error);
    }
  };

  const entrarTelaHome = async () => {
    try {
      const response = await axios.post(BASE_URL + "/login", {
        usuario: usuario,
        senha: senha,
      });

      console.log(response);

      if (response.status === 200) {
        navigation.navigate("TelaHome");
        setCookie(usuario);
      } else {
        setModalVisible(true);
      }
    } catch (error) {
      setModalVisible(true);
      console.log(error);
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
    container: {
      flex: 1,
      flexDirection: "row",
    },
    halfContainer: {
      flex: 1,
    },
    rightHalfContent: {
      flex: 1,
      justifyContent: "center",
      alignItems: "center",
      marginTop: isMobile ? -180 : 0,
    },
    textLogin: {
      fontSize: 60,
      fontFamily: "LuckiestGuy",
      marginBottom: 10,
      color: "#B20000",
    },
    backImage: {
      flex: 2,
      justifyContent: "center",
      width: "100%",
      height: "100%",
    },
    input: {
      width: "80%",
      height: 40,
      borderWidth: 1,
      borderColor: "#ccc",
      marginBottom: 10,
      paddingHorizontal: 10,
      borderRadius: 4,
      shadowColor: "#000",
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.2,
      shadowRadius: 4,
    },
    inputContainer: {
      flexDirection: "row",
      alignItems: "center",
      width: "80%",
      marginBottom: 10,
      borderWidth: 1,
      borderColor: "#ccc",
      borderRadius: 4,
      paddingHorizontal: 10,
      shadowColor: "#000",
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.2,
      shadowRadius: 4,
    },
    inputSenha: {
      flex: 1,
      height: 40,
    },
    button: {
      backgroundColor: "#015500",
      paddingVertical: 10,
      paddingHorizontal: 20,
      borderRadius: 5,
      marginTop: 15,
    },
    SistemaTitulo: {
      fontFamily: "LuckiestGuy",
      fontSize: 80,
      color: "white",
      fontWeight: "bold",
    },
    SistemaSubTitulo: {
      fontFamily: "LuckiestGuy",
      fontSize: 40,
      color: "white",
    },
    buttonText: {
      color: "white",
      fontSize: 20,
      fontWeight: "bold",
    },
    imageLogo: {
      width: 300,
      height: 300,
      resizeMode: "contain",
    },
    centerImage: {
      position: "absolute",
      top: "50%",
      left: "65%",
      transform: [{ translateX: -200 }, { translateY: -10 }],
    },
    bottomImageMobile: {
      position: "absolute",
      bottom: 90,
      alignSelf: "center",
      left: "50%",
      transform: [{ translateX: -150 }]
    },
    icon: {
      padding: 5,
    },
  });

  return (
    <View style={styles.container}>
      <CustomModal
        modalVisible={modalVisible}
        setModalVisible={setModalVisible}
        modalText="Credenciais Inválidas"
      />
      {!isMobile && (
      <ImageBackground
        source={require("../../assets/images/bg-opaco.png")}
        resizeMode="cover"
        style={styles.backImage}
      >
        <View
          style={{
            flex: 2,
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            backgroundColor: "rgba(178,0,0,0.7)",
          }}
        >
          <View>
            <Text style={styles.SistemaTitulo}>Gestão de Entregas</Text>
            <Text style={styles.SistemaSubTitulo}>Casa Zé Rissi</Text>
          </View>
        </View>
      </ImageBackground>
    )}
      
      <View style={{ flex: 1, backgroundColor: "white" }}>
        <View style={styles.rightHalfContent}>
          <Text style={styles.textLogin}> Login </Text>
          <TextInput
            style={styles.input}
            placeholder="Usuário"
            value={usuario}
            onChangeText={(text) => setUsuario(text)}
            testID="login-input"
          />

          <View style={styles.inputContainer}>
            <TextInput
              style={styles.inputSenha}
              placeholder="Senha"
              value={senha}
              onChangeText={(text) => setSenha(text)}
              secureTextEntry={!showPassword} 
              testID="senha-input"
            />
            <TouchableOpacity
              onPress={() => setShowPassword((prev) => !prev)}
              style={styles.icon}
              testID="mostrar-senha-btn"
            >
              <MaterialIcons
                name={showPassword ? "visibility-off" : "visibility"}
                size={24}
                color="gray"
              />
            </TouchableOpacity>
          </View>
          <Pressable onPress={entrarTelaHome} style={styles.button} testID="entrar-btn">
            <Text style={styles.buttonText}>Entrar</Text>
          </Pressable>
        </View>
      </View>
      
    {!isMobile && (
      <Image
      source={require("../../assets/images/logo.png")}
      style={[styles.imageLogo, isMobile ? styles.bottomImageMobile : styles.centerImage]}
    />
    )}
  </View>  
)
};




export default TelaLogin;
