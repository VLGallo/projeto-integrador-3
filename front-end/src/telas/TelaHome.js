import React, { useState, useEffect, useContext } from "react";
import {
  View,
  Text,
  StyleSheet,
  ImageBackground,
  Dimensions,
} from "react-native";
import Template from "../components/TemplatePrincipal";
import { useTheme } from "../context/ThemeContext";
import { BASE_URL } from '@env';


const TelaHome = () => {
  const [isMobile, setIsMobile] = useState(false);
  const { isDarkMode } = useTheme();
  const theme = isDarkMode ? "light" : "dark";




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

  return (
    <Template>
      <ImageBackground
        source={
          isMobile
            ? require("../../assets/images/imagem-home-mobile.jpg")
            : require("../../assets/images/imagem-home.jpg")
        }
        resizeMode="cover"
        style={styles.backImage}
      >
        <View style={styles.tituloContainer}>
          <Text style={[styles.textHome, { fontSize: isMobile ? 48 : 80, marginTop: 80 }]}>
            Gestão de Entregas
          </Text>
          <View style={{ height: "80vh" }} />
        </View>
      </ImageBackground>
    </Template>
  );
};

const styles = StyleSheet.create({
  textHome: {
    color: "#ffffff",
    textAlign: "center",
    fontFamily: "LuckiestGuy",
    fontWeight: "bold",
  },
  backImage: {
    flex: 2,
    justifyContent: "center",
    width: "100%",
    height: "100%",
  },
  tituloContainer: {
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 20,
  },
});

export default TelaHome;
