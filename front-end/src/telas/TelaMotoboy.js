// TelaMotoboy.jsx

import React, { useState, useEffect } from 'react';
import {
  SafeAreaView,
  ScrollView,
  Text,
  Image,
  View,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  Pressable,
} from 'react-native';
import { useTheme } from '../context/ThemeContext';
import TemplateMotoboy from "../components/TemplateMotoboy";
import CustomizedSwitches from '../components/MaterialSwitch';
import CustomModal from "../components/CustomModal";
import { useNavigation } from "@react-navigation/native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { BASE_URL } from '@env';
import { useRoute } from "@react-navigation/native";
import { getMotoboyStyles } from '../components/styles/StyleSheetMotoboy';


const TelaMotoboy = () => {
  const isMobile = Dimensions.get('window').width < 768;
  const [pedidos, setPedidos] = useState([]);
  const [entregasFeitas, setEntregasFeitas] = useState(0);
  const [valorReceber, setValorReceber] = useState(0.00);
  const [modalVisible, setModalVisible] = useState(true);
  const { isDarkMode, toggleTheme } = useTheme();
  const navigation = useNavigation();
  const route = useRoute();
  const { motoboyId } = route.params || {};


  const styles = getMotoboyStyles(isDarkMode);

  const [modalText, setModalText] = useState('');
const [motoboy, setMotoboy] = useState({ nome: '' });

useEffect(() => {
  const buscarMotoboy = async () => {
    try {
      const motoboyString = await AsyncStorage.getItem('motoboy');
      if (motoboyString) {
        const motoboyData = JSON.parse(motoboyString);
        setMotoboy(motoboyData);
        setModalText(`Bem-vindo, ${motoboyData.nome}! Pronto para mais entregas?`);
        setModalVisible(true); // Abre o modal = "motoboy-welcome-text-btn"
      }
    } catch (error) {
      console.log('Erro ao buscar motoboy:', error);
    }
  };

  buscarMotoboy();
}, []);



  useEffect(() => {
    if (motoboyId) {
      buscarPedidos(motoboyId);
    } else {
      console.error('Motoboy ID não encontrado!');
    }
  }, [motoboyId]);

  // Função para sair e ir para tela de login
  const handleSair = async () => {
    try {
      await AsyncStorage.removeItem("usuario");
      console.log("Usuário deslogado com sucesso");
      navigation.navigate("TelaLogin");
    } catch (error) {
      console.error("Erro ao sair:", error);
    }
  };


  const buscarPedidos = async (id) => {
    try {
      const response = await fetch(`${BASE_URL}/pedido/motoboy/${id}`);
      if (!response.ok) {
        console.error('Erro ao buscar os pedidos');
        return;
      }

      const data = await response.json();

      const hoje = new Date().toISOString().split('T')[0];

      const pedidosDoDia = data.filter(pedido => {
        if (!pedido.data_hora_inicio) return false;

        const dataPedido = new Date(pedido.data_hora_inicio);
        if (isNaN(dataPedido)) return false;

        return dataPedido.toISOString().split('T')[0] === hoje;
      });

      setPedidos(pedidosDoDia);

      const entreguesHoje = pedidosDoDia.filter(p => p.status === 'Entregue');
      setEntregasFeitas(entreguesHoje.length);

      const totalReceberHoje = entreguesHoje.reduce((acc, pedido) => acc + parseFloat(pedido.total_pedido || 0), 0);
      setValorReceber(totalReceberHoje);

      console.log('Pedidos do dia:', pedidosDoDia);
    } catch (error) {
      console.error('Erro ao buscar pedidos:', error);
    }
  };


  const atualizarStatusPedido = async (id, action) => {
    try {
      const response = await fetch(`${BASE_URL}/pedido/${id}/action/${action}`, {
        // usa POST para ambas as ações
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Erro ao atualizar o pedido');
      }

      const pedidoAtualizado = await response.json();
      console.log('Pedido atualizado:', pedidoAtualizado);

      setPedidos((prevPedidos) =>
        prevPedidos.map((pedido) =>
          pedido.id === id ? pedidoAtualizado : pedido
        )
      );

      if (action === 'entregar' || action === 'cancelar') {
        buscarPedidos(motoboyId);
      }

    } catch (error) {
      console.error('Erro ao atualizar pedido:', error);
    }
  };


  const formatarEndereco = (cliente) => {
    if (!cliente) return '';
  
    const {
      logradouro = '',
      numero = '',
      complemento = '',
      bairro = '',
      cep = '',
    } = cliente;
  
    return `${logradouro}, ${numero}${complemento ? ' - ' + complemento : ''} - ${bairro} - CEP: ${cep}`;
  };
  


  return (
    <TemplateMotoboy>
      <SafeAreaView style={styles.container}>

        {/* Modal */}
        <CustomModal
          modalVisible={modalVisible}
          setModalVisible={setModalVisible}
          modalText={modalText}
          testIDText="motoboy-welcome-text"  // Test ID para o texto
          testIDButton="modal-ok-btn"       // Test ID para o botão
        />

        {/* Título + Switch no topo */}
        <View style={styles.headerContainer}>
          <View style={{ flex: 2, alignItems: 'center', flexDirection: 'row', justifyContent: 'center' }}>
            <Text style={[styles.titulo, { fontFamily: 'LuckiestGuy', color: '#B20000' }]}>
              Pedidos{motoboy?.nome ? ` - ${motoboy.nome}` : ''}
            </Text>
          </View>
          <CustomizedSwitches checked={isDarkMode} onChange={toggleTheme} />
        </View>

        {/* Conteúdo principal */}
        <View style={styles.conteudo}>
          <View style={styles.areaScroll}>
          <ScrollView
              data-testid='scroll-pedidos'
              contentContainerStyle={styles.scrollContainer}
              style={{
                scrollbarColor: isDarkMode ? '#888 #222' : '#999 #fff', // thumb | track
                scrollbarWidth: 'thin',
              }}
            >

              {[...pedidos]
                .sort((a, b) => a.id - b.id) // crescente (do menor para o maior). Use `b.id - a.id` para ordem decrescente.
                .map((pedido) => {
              const statusNormalizado = pedido.status?.toLowerCase();

              return (
                <View
                  key={pedido.id}
                  style={[
                    styles.cardPedido,
                    (statusNormalizado === 'entregue' || statusNormalizado === 'cancelado') && styles.cardEntregue
                  ]}
                >
                  <View style={styles.pedidoInfo}>
                    <Text style={styles.pedidoTitulo}>Pedido {pedido.id}</Text>
                    <Text style={styles.descricao}>Cliente: {pedido.cliente?.nome ?? 'Desconhecido'}</Text>
                    <Text style={styles.descricao}>Endereço: {formatarEndereco(pedido.cliente)}</Text>
                    <Text style={styles.descricao}>Telefone: {pedido.cliente?.telefone ?? 'Sem telefone'}</Text>
                    <Text style={styles.descricao}>Total: R${pedido.total_pedido?.toFixed(2) ?? '0.00'}</Text>

                    <Text
                      style={[
                        styles.statusTexto,
                        statusNormalizado === 'entregue' && styles.statusEntregue,
                        statusNormalizado === 'cancelado' && styles.statusCancelado,
                        statusNormalizado === 'em andamento' && styles.statusPendente
                      ]}
                    >
                      Status: {pedido.status}
                    </Text>
                  </View>

                  <View style={styles.botoesContainer}>
                    {statusNormalizado === 'em andamento' && (
                      <>
                        <Pressable
                          accessibilityLabel="entregar-pedido-btn"
                          onPress={() => atualizarStatusPedido(pedido.id, 'entregar')}
                          style={styles.botaoVerde}
                        >
                          <Text styl  e={styles.textoBotao}>✔️</Text>
                      </Pressable>


                        <Pressable
                          accessibilityLabel="cancelar-pedido-btn"
                          onPress={() => atualizarStatusPedido(pedido.id, 'cancelar')}
                          style={styles.botaoCinza}
                          >
                          <Text style={styles.textoBotao}>❌</Text>
                        </Pressable>
                      </>
                    )}
                  </View>
                </View>
              );
            })}

            </ScrollView>
          </View>

          <View style={styles.areaResumo}>
            <Image source={require('../../assets/favicon.png')} style={styles.faviconIcon} />

            {!isMobile && (
              <View style={styles.colunasResumo}>
                <View style={styles.colunaItem}>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoTexto}>Entregas</Text>
                  </View>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoValor}>{entregasFeitas}</Text>
                  </View>
                </View>

                <View style={styles.colunaItem}>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoTexto}>Valor a receber</Text>
                  </View>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoValor}>R$ {(entregasFeitas * 5).toFixed(2)}</Text>
                  </View>
                </View>

                <View style={styles.colunaItem}>
                  <Image source={require('../../assets/images/pizza.png')} style={styles.pizzaIcon} />
                </View>
              </View>
            )}

            {isMobile && (
              <View style={styles.colunasResumo}>
                <View style={styles.colunaItem}>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoTexto}>Entregas</Text>
                  </View>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoValor}>{entregasFeitas}</Text>
                  </View>
                </View>

                <View style={styles.colunaItem}>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoTexto}>Valor a receber</Text>
                  </View>
                  <View style={styles.caixaBranca}>
                    <Text style={styles.resumoValor}>R$ {(entregasFeitas * 5).toFixed(2)}</Text>
                  </View>
                </View>
              </View>
            )}

            {/* Ícone da pizza isolado se for mobile */}
            {isMobile && (
              <Image source={require('../../assets/images/pizza.png')} style={styles.pizzaIcon} />
            )}

            {/* Botão Sair */}
            <View style={{ alignItems: 'center', marginTop: 20 }}>
              <TouchableOpacity
                style={{
                  backgroundColor: '#B20000',
                  paddingHorizontal: 40,
                  paddingVertical: 12,
                  borderRadius: 10,
                }}
                onPress={handleSair}
              >
                <Text style={{ color: '#fff', fontWeight: 'bold', fontSize: 16 }}>Sair</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </SafeAreaView>
    </TemplateMotoboy>
  );
};

export default TelaMotoboy;
