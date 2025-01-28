import React, { useEffect, useState } from "react";
import {
  View,
  Pressable,
  StyleSheet,
  ImageBackground,
  Dimensions,
} from "react-native";
import { MaterialIcons } from "@expo/vector-icons";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import SideNavigation from "../components/SideNavigation";
import { useTheme } from "../context/ThemeContext";

const Template = ({ children }) => {
  const [isMobile, setIsMobile] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
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

  const toggleDrawer = (open) => () => {
    setDrawerOpen(open);
  };

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      <List>
        <SideNavigation />
      </List>
      <Divider />
    </Box>
  );

  const styles = StyleSheet.create({
    containerPrincipal: {
      flex: 1,
      backgroundColor: isDarkMode ? "#FFF" : "#000",
      flexDirection: "row",
    },
    leftContainer: {
      flex: 2,
      width: "100%",
      alignItems: "center",
      justifyContent: "center",
    },
    backImage: {
      flex: 2,
      justifyContent: "center",
      width: "100%",
      height: "100%",
    },
    menuIcon: {
      position: "absolute",
      top: 40,
      right: 20,
      zIndex: 10,
    }
  });

  return (
    <View style={styles.containerPrincipal}>
      {isMobile && (
        <Pressable style={styles.menuIcon} onPress={toggleDrawer(true)}>
          <MaterialIcons name="menu" size={32} color="black" />
        </Pressable>
      )}

      <ImageBackground
        source={require("../../assets/images/bg-opaco.png")}
        resizeMode="cover"
        style={styles.backImage}
      >
        <View style={styles.leftContainer}>{children}</View>
      </ImageBackground>

      {!isMobile && (
        <View style={styles.rightContainer}>
          <SideNavigation />
        </View>
      )}

      {/* Definimos `anchor="right"` para que o drawer abra do lado direito */}
      <Drawer anchor="right" open={drawerOpen} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
    </View>
  );
};

export default Template;
