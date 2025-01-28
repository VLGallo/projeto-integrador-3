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

export default function TransferList({ pedidos, setSelectedPedidos }) {
  const [checked, setChecked] = React.useState([]);
  const [left, setLeft] = React.useState(pedidos);
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
    setSelectedPedidos(newRight.map((pedido) => pedido.id));
  };

  const handleCheckedRight = () => {
    const newRight = right.concat(leftChecked);
    setRight(newRight);
    setLeft(not(left, leftChecked));
    setChecked(not(checked, leftChecked));
    setSelectedPedidos(newRight.map((pedido) => pedido.id));
  };

  const handleCheckedLeft = () => {
    setLeft(left.concat(rightChecked));
    setRight(not(right, rightChecked));
    setChecked(not(checked, rightChecked));
  };

  const handleAllLeft = () => {
    setLeft(left.concat(right));
    setRight([]);
    setSelectedPedidos([]);
  };

  const customList = (items) => (
    <Paper
      sx={{
        width: 128,
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
    >
      <List dense component="div" role="list">
        {items.map((value) => {
          const labelId = `transfer-list-item-${value.id}-label`;

          return (
            <ListItemButton
              key={value.id}
              role="listitem"
              onClick={handleToggle(value)}
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
                  sx={{
                    color: isDarkMode ? "#000" : "#fff",
                  }}
                  data-testid={{
                    "aria-labelledby": labelId,
                  }}
                />
              </ListItemIcon>
              <ListItemText
                id={labelId}
                primary={`${value.id}`}
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
      <Grid item>{customList(left)}</Grid>
      <Grid item>
        <Grid container direction="column" sx={{ alignItems: "center" }}>
          <Button
            sx={{ my: 0.5 }}
            variant="contained"
            size="small"
            color="success"
            onClick={handleAllRight}
            disabled={left.length === 0}
            data-testid="adicionar-todos-btn"
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
            data-testid="adicionar-um-btn"
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
            data-testid="remover-um-btn"
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
            data-testid="remover-todos-btn"
          >
            ≪
          </Button>
        </Grid>
      </Grid>
      <Grid item>{customList(right)}</Grid>
    </Grid>
  );
}
