import React, { useState, useEffect } from "react";
import { View, Text, StyleSheet, Image, Dimensions } from "react-native";
import Template from "../components/TemplatePrincipal";
import axios from "axios";
import { useTheme } from "../context/ThemeContext";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import { BASE_URL } from "@env";

const TelaRelatorio = () => {
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode, toggleTheme } = useTheme();
  const [motoboys, setMotoboys] = useState([]);
  const [pedidosDoDia, setPedidosDoDia] = useState([]);
  const [carregandoMotoboys, setCarregandoMotoboys] = useState(false);
  const [carregandoPedidosDoDia, setCarregandoPedidosDoDia] = useState("");

  useEffect(() => {
    const carregarPedidosDoDia = async () => {
      try {
        setCarregandoPedidosDoDia(true);
        const response = await axios.get(BASE_URL + "/pedido/motoboys");

        const dataAtual = new Date().toISOString().slice(0, 10); // Formato "YYYY-MM-DD"

        const pedidosEntreguesHoje = Object.values(response.data).flatMap((motoboy) =>
          motoboy.pedidos.filter(
            (pedido) =>
              pedido.status === "Entregue" && 
              pedido.data_hora_finalizacao &&
              pedido.data_hora_finalizacao.slice(0, 10) === dataAtual
          )
        );

 
        const groupedPedidos = pedidosEntreguesHoje.reduce((acc, pedido) => {
          const nomeMotoboy = pedido.motoboy?.nome || "N/A";
          if (!acc[nomeMotoboy]) {
            acc[nomeMotoboy] = {
              nome: nomeMotoboy,
              pedidos: [],
            };
          }
          acc[nomeMotoboy].pedidos.push(pedido);
          return acc;
        }, {});

        // Convertendo o objeto para um array de motoboys com pedidos agrupados
        const pedidosAgrupados = Object.values(groupedPedidos);

        setPedidosDoDia(pedidosAgrupados);
        setCarregandoPedidosDoDia(false);
      } catch (error) {
        console.log(error);
      }
    };
    carregarPedidosDoDia();
  }, []);

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
    image: {
      width: 80,
      height: 100,
    },
    textRelatorio: {
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
    posicaoImage: {
      marginLeft: 20,
    },
    menuSuperior: {
      flexDirection: "row",
      justifyContent: "center",
      alignItems: "center",
      marginTop: 20,
    },
    menuButton: {
      backgroundColor: "#015500",
      borderRadius: 10,
      paddingVertical: 10,
      paddingHorizontal: 20,
      marginRight: 10,
    },
    menuButtonText: {
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
    Tabela: {
      fontSize: 16,
    },
  });

  return (
    <Template imagem={"../../assets/images/bg-opaco.png"}>
      <View style={[styles.containerSecundario, { margin: 30 }]}>
        <View style={styles.tituloContainer}>
          <Text
            style={[
              styles.textRelatorio,
              { fontSize: isMobile ? 30 : 60, marginTop: 30 },
            ]}
          >
            Relatório de Entregas
          </Text>
        </View>
      </View>

      <View style={{ flexDirection: "row", alignItems: "center" }}>
        {!carregandoPedidosDoDia && (
          <View style={styles.container}>
            <TableContainer
              component={Paper}
              style={{
                backgroundColor: isDarkMode ? "#fff" : "#434141",
                marginHorizontal: "auto",
              }}
            >
              <Table style={styles.tabela}>
                <TableHead>
                  <TableRow>
                    <TableCell
                      style={{
                        fontSize: isMobile ? 14 : 20,
                        fontWeight: "bold",
                        color: isDarkMode ? "#000" : "#fff",
                        padding: isMobile ? 4 : 16,
                        textAlign: "center",
                      }}
                    >
                      Motoboy
                    </TableCell>
                    <TableCell
                      style={{
                        fontSize: isMobile ? 14 : 20,
                        fontWeight: "bold",
                        color: isDarkMode ? "#000" : "#fff",
                        padding: isMobile ? 4 : 16,
                        textAlign: "center",
                      }}
                    >
                      Pedido
                    </TableCell>
                    <TableCell
                      style={{
                        fontSize: isMobile ? 14 : 20,
                        fontWeight: "bold",
                        color: isDarkMode ? "#000" : "#fff",
                        padding: isMobile ? 4 : 16,
                        textAlign: "center",
                      }}
                    >
                      Finalização
                    </TableCell>
                    <TableCell
                      style={{
                        fontSize: isMobile ? 14 : 20,
                        fontWeight: "bold",
                        color: isDarkMode ? "#000" : "#fff",
                        padding: isMobile ? 4 : 16,
                        textAlign: "center",
                      }}
                    >
                      Entregas
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {pedidosDoDia.map((motoboy, index) => (
                    <React.Fragment key={index}>
                      {motoboy.pedidos.map((pedido, i) => (
                        <TableRow key={i}>
                          {i === 0 && (
                            <>
                              <TableCell
                                rowSpan={motoboy.pedidos.length}
                                style={{
                                  fontSize: isMobile ? 14 : 18,
                                  color: isDarkMode ? "#000" : "#fff",
                                  padding: isMobile ? 4 : 16,
                                  textAlign: "center",
                                }}
                                data-testid="nomeMotoboy"
                              >
                                {motoboy.nome}
                              </TableCell>
                              <TableCell
                                style={{
                                  fontSize: isMobile ? 14 : 18,
                                  color: isDarkMode ? "#000" : "#fff",
                                  padding: isMobile ? 4 : 16,
                                  textAlign: "center",
                                }}
                              >
                                {pedido.id}
                              </TableCell>
                              <TableCell
                                style={{
                                  fontSize: isMobile ? 14 : 18,
                                  color: isDarkMode ? "#000" : "#fff",
                                  padding: isMobile ? 4 : 16,
                                  textAlign: "center",
                                }}
                              >
                                {pedido.data_hora_finalizacao
                                  ? new Date(
                                      pedido.data_hora_finalizacao
                                    ).toLocaleTimeString()
                                  : "-"}
                              </TableCell>
                              <TableCell
                                rowSpan={motoboy.pedidos.length}
                                style={{
                                  fontSize: isMobile ? 14 : 18,
                                  color: isDarkMode ? "#000" : "#fff",
                                  padding: isMobile ? 4 : 16,
                                  textAlign: "center",
                                }}
                              >
                                {motoboy.pedidos.length}
                              </TableCell>
                            </>
                          )}
                          {i > 0 && (
                            <>
                              <TableCell
                                style={{
                                  fontSize: isMobile ? 14 : 18,
                                  color: isDarkMode ? "#000" : "#fff",
                                  padding: isMobile ? 4 : 16,
                                  textAlign: "center",
                                }}
                              >
                                {pedido.id}
                              </TableCell>
                              <TableCell
                                style={{
                                  fontSize: isMobile ? 14 : 18,
                                  color: isDarkMode ? "#000" : "#fff",
                                  padding: isMobile ? 4 : 16,
                                  textAlign: "center",
                                }}
                              >
                                {pedido.data_hora_finalizacao
                                  ? new Date(
                                      pedido.data_hora_finalizacao
                                    ).toLocaleTimeString()
                                  : "-"}
                              </TableCell>
                            </>
                          )}
                        </TableRow>
                      ))}
                    </React.Fragment>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </View>
        )}

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

export default TelaRelatorio;
