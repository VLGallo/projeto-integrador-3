import React from 'react';
import { Modal, Text, View, Pressable, Alert, StyleSheet, Dimensions } from 'react-native';
import { useTheme } from '../context/ThemeContext';

const { width } = Dimensions.get('window');
const isSmallScreen = width < 768;

const CustomModal = ({ modalVisible, setModalVisible, modalText }) => {
  const { isDarkMode } = useTheme(); // Usando o contexto do tema

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={modalVisible}
      onRequestClose={() => {
        Alert.alert("Modal fechado.");
        setModalVisible(!modalVisible);
      }}
    >
      <View style={styles.centeredView}>
        <View style={[
          styles.modalView,
          isSmallScreen && styles.modalViewSmall,
          !isDarkMode && styles.modalDark // Estilo para o modo escuro
        ]}>
          <Text style={[
            styles.modalText,
            isSmallScreen && styles.modalTextSmall,
            !isDarkMode && styles.modalTextDark // Texto branco para o modo escuro
          ]}>
            {modalText}
          </Text>
          <View style={{ flexDirection: "row" }}>
            <Pressable
              onPress={() => setModalVisible(!modalVisible)}
              style={[
                styles.modalButton,
                !isDarkMode && styles.modalButtonDark // Botão no modo escuro
              ]}
            >
              <Text style={styles.buttonText}>Ok</Text>
            </Pressable>
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 22,
  },
  modalView: {
    margin: 20,
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 2, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalViewSmall: {
    width: 300,
    padding: 20,
  },
  modalDark: {
    backgroundColor: "#333", // Fundo preto para modo escuro
  },
  modalText: {
    marginBottom: 15,
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 20,
  },
  modalTextSmall: {
    fontSize: 16,
  },
  modalTextDark: {
    color: "#fff", // Texto branco para modo escuro
  },
  modalButton: {
    backgroundColor: "#B20000",
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  modalButtonDark: {
    backgroundColor: "#950000", // Cor mais escura para o botão no modo escuro
  },
  buttonText: {
    color: "#fff",
    fontWeight: "bold"
  }
});

export default CustomModal;
