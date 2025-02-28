import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image, ScrollView, SafeAreaView } from 'react-native';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';
import { BASE_URL } from '@env';

const TelaMotoboy = ({ route }) => {
  const { motoboyId } = route.params || {};
  const [motoboy, setMotoboy] = useState(null);
  const [pedidos, setPedidos] = useState([]);
  const [entregasFeitas, setEntregasFeitas] = useState(0);
  const navigation = useNavigation();

  useEffect(() => {
    if (motoboyId) {
      buscarPedidos(motoboyId);
    } else {
      console.error('Motoboy ID não encontrado!');
    }
  }, [motoboyId]);

  const buscarPedidos = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/pedido/motoboy/${id}`);
      if (!response.ok) {
        console.error('Erro ao buscar os pedidos');
        return;
      }
      const data = await response.json();
      setPedidos(data);
      setEntregasFeitas(data.filter(p => p.status === 'Entregue').length);
      console.log(data);
      console.log(data.filter(p => p.status === 'Entregue').length);
    } catch (error) {
      console.error('Erro ao buscar pedidos:', error);
    }
  };

  const atualizarStatusPedido = async (idPedido, acao) => {
    try {
      await axios.post(`${BASE_URL}/pedido/${idPedido}/action/${acao}`);
      console.log(`Pedido ${idPedido} atualizado com sucesso!`);
      buscarPedidos(motoboyId);
    } catch (error) {
      console.error('Erro ao atualizar pedido:', error);
    }
  };

  const handleSair = () => {
    navigation.navigate("TelaLogin");
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#b20000' }}>
      <ScrollView contentContainerStyle={{ flexGrow: 1 }}>
        <View style={styles.container}>
          <Text style={styles.header}>Entregas</Text>
          {motoboy && <Text style={styles.motoboyName}>{motoboy.nome}</Text>}
          <Image source={require('../../assets/images/pizza.png')} style={styles.image} />

          {/* Quadro com os pedidos que será rolável */}
          <View style={styles.pedidosContainer}>
            <ScrollView style={styles.pedidosScroll}>
              {pedidos.map((item) => (
                <View key={item.id} style={styles.pedidoInfo}>
                  <Text style={styles.pedidoText}>Pedido: {item.id}</Text>
                  <Text style={styles.pedidoText}>Total: R${item.total_pedido.toFixed(2)}</Text>
                  <Text style={styles.pedidoText}>Status: {item.status}</Text>
                  {item.status === 'Em andamento' && (
                    <View style={styles.buttonsContainer}>
                      <TouchableOpacity onPress={() => atualizarStatusPedido(item.id, 'entregar')} style={styles.button}>
                        <Text style={styles.buttonText}>Entregar</Text>
                      </TouchableOpacity>
                      <TouchableOpacity onPress={() => atualizarStatusPedido(item.id, 'cancelar')} style={[styles.button, styles.cancelButton]}>
                        <Text style={styles.buttonText}>Cancelar</Text>
                      </TouchableOpacity>
                    </View>
                  )}
                </View>
              ))}
            </ScrollView>
          </View>

          {/* Rodapé com total de entregas */}
          <View style={styles.footer}>
            <Text style={styles.entregasText}>Entregas feitas: {entregasFeitas}</Text>
            <Text style={styles.entregasText}>Valor a receber: R${(entregasFeitas * 5).toFixed(2)}</Text>
            <TouchableOpacity onPress={handleSair} style={styles.logoutButton} testID="sair-btn">
              <Text style={styles.logoutButtonText}>Sair</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
    flexGrow: 1,
  },
  header: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 20,
    textAlign: 'center',
  },
  motoboyName: {
    fontSize: 22,
    color: '#fff',
    marginBottom: 10,
    textAlign: 'center',
  },
  image: {
    width: 100,
    height: 100,
    alignSelf: 'center',
    marginBottom: 20,
  },
  pedidosContainer: {
    backgroundColor: '#fff',
    padding: 10,
    marginVertical: 10,
    borderRadius: 8,
    height: 300, // Define a altura máxima do quadro rolável
  },
  pedidosScroll: {
    height: '100%', // Faz com que o scroll ocupe a área inteira do quadro
  },
  pedidoInfo: {
    backgroundColor: '#f7f7f7',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
  },
  pedidoText: {
    fontSize: 16,
    marginBottom: 5,
  },
  buttonsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  button: {
    backgroundColor: 'green',
    padding: 10,
    borderRadius: 5,
  },
  cancelButton: {
    backgroundColor: 'red',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  entregasText: {
    fontSize: 18,
    color: '#fff',
    marginTop: 10,
    textAlign: 'center',
  },
  footer: {
    marginBottom: 40,
    alignItems: 'center',
  },
  logoutButton: {
    marginTop: 20,
    backgroundColor: '#000',
    padding: 10,
    borderRadius: 5,
  },
  logoutButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default TelaMotoboy;
