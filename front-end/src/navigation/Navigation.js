import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import TelaLogin from "../telas/TelaLogin";
import TelaHome from "../telas/TelaHome";
import TelaPedido from "../telas/TelaPedido";
import TelaAtribuicao from "../telas/TelaAtribuicao";
import TelaCadastro from "../telas/TelaCadastro";
import TelaRelatorio from "../telas/TelaRelatorio";
import TelaCliente from "../telas/TelaCliente";

const Stack = createStackNavigator();

const Navigation = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="TelaLogin">
        <Stack.Screen
          name="TelaLogin"
          component={TelaLogin}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TelaHome"
          component={TelaHome}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TelaPedido"
          component={TelaPedido}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TelaAtribuicao"
          component={TelaAtribuicao}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TelaCadastro"
          component={TelaCadastro}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TelaRelatorio"
          component={TelaRelatorio}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TelaCliente" // Registrando a nova tela
          component={TelaCliente}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default Navigation;
