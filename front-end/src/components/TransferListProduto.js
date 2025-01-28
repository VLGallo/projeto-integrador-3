import * as React from "react";
import Grid from "@mui/material/Grid";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import { useTheme } from "../context/ThemeContext";

function not(a, b) {
  return a.filter((value) => !b.includes(value));
}

function intersection(a, b) {
  return a.filter((value) => b.includes(value));
}

export default function TransferList({ produtos, setSelectedProdutos }) {
  const [checked, setChecked] = React.useState([]);
  const [left, setLeft] = React.useState(produtos);
  const [right, setRight] = React.useState([]);

  const leftChecked = intersection(checked, left);
  const rightChecked = intersection(checked, right);

  const { isDarkMode } = useTheme();

  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) {
      newChecked.push(value);
    } else {
      newChecked.splice(currentIndex, 1);
    }

    setChecked(newChecked);
  };

  const handleAllRight = () => {
    const newRight = right.concat(left);
    setRight(newRight);
    setLeft([]);
    setSelectedProdutos(
      newRight.map((produto) => ({
        id: produto.id,
        nome: produto.nome,
      }))
    );
  };

  const handleCheckedRight = () => {
    const newRight = right.concat(leftChecked);
    setRight(newRight);
    setLeft(not(left, leftChecked));
    setChecked(not(checked, leftChecked));
    setSelectedProdutos(
      newRight.map((produto) => ({
        id: produto.id,
        nome: produto.nome,
      }))
    );
  };

  const handleCheckedLeft = () => {
    setLeft(left.concat(rightChecked));
    setRight(not(right, rightChecked));
    setChecked(not(checked, rightChecked));
  };

  const handleAllLeft = () => {
    setLeft(left.concat(right));
    setRight([]);
    setSelectedProdutos([]);
  };

  const customList = (items, listType) => (
    <Paper
      sx={{
        width: 200,
        height: 200,
        overflow: "auto",
        backgroundColor: isDarkMode ? "#fff" : "#434141",
        color: isDarkMode ? "#fff" : "#000",
        "&::-webkit-scrollbar": {
          width: 12,
        },
        "&::-webkit-scrollbar-track": {
          backgroundColor: isDarkMode ? "#f0f0f0" : "#2e2e2e",
        },
        "&::-webkit-scrollbar-thumb": {
          backgroundColor: isDarkMode ? "#6b6b6b" : "#c1c1c1",
        },
      }}
      data-testid={`list-${listType}`}
    >
      <List dense component="div" role="list">
        {items.map((value) => {
          const labelId = `transfer-list-item-${value.id}-label`;

          return (
            <ListItemButton
              key={value.id}
              role="listitem"
              onClick={handleToggle(value)}
              data-testid={`list-item-${value.id}`}
              sx={{
                backgroundColor: isDarkMode ? "#fff" : "#434141",
                color: isDarkMode ? "#000" : "#fff",
                "&:hover": {
                  backgroundColor: isDarkMode ? "#f0f0f0" : "#5a5a5a",
                },
              }}
            >
              <ListItemIcon>
                <Checkbox
                  checked={checked.includes(value)}
                  tabIndex={-1}
                  disableRipple
                  data-testid={`checkbox-${listType}-${value.id}`}
                  sx={{
                    color: isDarkMode ? "#000" : "#fff",
                  }}
                  inputProps={{
                    "aria-labelledby": labelId,
                  }}
                />
              </ListItemIcon>
              <ListItemText
                id={labelId}
                primary={`${value.nome}`}
                sx={{ color: isDarkMode ? "#000" : "#fff" }}
              />
            </ListItemButton>
          );
        })}
      </List>
    </Paper>
  );

  return (
    <Grid
      container
      spacing={2}
      sx={{ justifyContent: "left", alignItems: "center" }}
    >
      <Grid item>{customList(left, "left")}</Grid>
      <Grid item>
        <Grid container direction="column" sx={{ alignItems: "center" }}>
          <Button
            sx={{ my: 0.5 }}
            variant="contained"
            size="small"
            color="success"
            onClick={handleAllRight}
            disabled={left.length === 0}
            data-testid="move-all-right-btn"
          >
            ≫
          </Button>
          <Button
            sx={{ my: 0.5 }}
            variant="contained"
            size="small"
            color="success"
            onClick={handleCheckedRight}
            disabled={leftChecked.length === 0}
            data-testid="move-selected-right-btn"
          >
            &gt;
          </Button>
          <Button
            sx={{ my: 0.5 }}
            variant="contained"
            size="small"
            color="success"
            onClick={handleCheckedLeft}
            disabled={rightChecked.length === 0}
            data-testid="move-selected-left-btn"
          >
            &lt;
          </Button>
          <Button
            sx={{ my: 0.5 }}
            variant="contained"
            size="small"
            color="success"
            onClick={handleAllLeft}
            disabled={right.length === 0}
            data-testid="move-all-left-btn"
          >
            ≪
          </Button>
        </Grid>
      </Grid>
      <Grid item>{customList(right, "right")}</Grid>
    </Grid>
  );
}
