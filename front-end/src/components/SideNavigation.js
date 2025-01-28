import React from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import MaterialSwitch from "../components/MaterialSwitch";
import { useTheme } from "../context/ThemeContext";

const SideNavigation = () => {
  const navigation = useNavigation();

  // Pega o estado e a função de alternância do contexto
  const { isDarkMode, toggleTheme } = useTheme();

  const entrarTelaHome = () => {
    navigation.navigate("TelaHome");
  };

  const entrarTelaCliente = () => {
    navigation.navigate("TelaCliente");
  };

  const entrarTelaPedido = () => {
    navigation.navigate("TelaPedido");
  };

  const entrarTelaAtribuicao = () => {
    navigation.navigate("TelaAtribuicao");
  };

  const entrarTelaCadastro = () => {
    navigation.navigate("TelaCadastro");
  };

  const entrarTelaRelatorio = () => {
    navigation.navigate("TelaRelatorio");
  };

  const destroyCookie = () => {
    try {
      AsyncStorage.removeItem("usuario");
      console.log("Cookie destruído com sucesso");
    } catch (error) {
      console.error("Erro ao destruir o cookie:", error);
    }
  };

  const handleSair = () => {
    destroyCookie();
    navigation.navigate("TelaLogin");
  };

  return (
    <>
      <View style={[styles.container, { margin: 30 }]}>
        <View style={[styles.switch]}>
          {/* Usa o toggleTheme diretamente do contexto */}
          <MaterialSwitch testID="darkmode-switch" onChange={toggleTheme} />
        </View>
        <Pressable
          onPress={entrarTelaHome}
          style={styles.button}
          testID="home-btn"
        >
          <Text style={styles.buttonText}>Home</Text>
        </Pressable>

        <Pressable
          onPress={entrarTelaCliente}
          style={styles.button}
          testID="cliente-btn"
        >
          <Text style={styles.buttonText}>Cliente</Text>
        </Pressable>

        <Pressable
          onPress={entrarTelaPedido}
          style={styles.button}
          testID="pedido-btn"
        >
          <Text style={styles.buttonText}>Pedido</Text>
        </Pressable>
        <Pressable
          onPress={entrarTelaAtribuicao}
          style={styles.button}
          testID="atribuicao-btn"
        >
          <Text style={styles.buttonText}>Atribuição</Text>
        </Pressable>
        <Pressable
          onPress={entrarTelaRelatorio}
          style={styles.button}
          testID="relatorio-btn"
        >
          <Text style={styles.buttonText}>Relatório</Text>
        </Pressable>
        <Pressable
          onPress={entrarTelaCadastro}
          style={styles.button}
          testID="cadastro-btn"
        >
          <Text style={styles.buttonText}>Cadastro</Text>
        </Pressable>

        <Pressable
          onPress={handleSair}
          style={[styles.button, { backgroundColor: "#B20000" }]}
          testID="sair-btn"
        >
          <Text style={styles.buttonText}>Sair</Text>
        </Pressable>
      </View>
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
    alignItems: "left",
    justifyContent: "left",
  },
  switch: {
    marginBottom: 20,
  },
  image: {
    flex: 1,
    width: "100%",
    height: "100%",
  },
  button: {
    width: 200,
    height: 50,
    backgroundColor: "#015500",
    marginBottom: 10,
    alignItems: "center",
    justifyContent: "center",
    borderRadius: 10,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
  },
});

export default SideNavigation;
