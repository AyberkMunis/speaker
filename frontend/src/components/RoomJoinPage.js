import React,{Component} from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { CssBaseline, InputLabel, MenuItem, Select, ThemeProvider } from "@material-ui/core";
import { createTheme } from '@material-ui/core/styles';
import { Image } from 'mui-image'

const theme = createTheme({
    palette: {
      primary: {
        main:"#191414",
      },
      secondary: {
        main: "#ffffff",
      },
      text:{
        primary:"#191414"

      }
    },
  });
export default class RoomJoinPage extends Component{
    constructor(props){
        super(props);
        this.state={
            roomCode:"",
            error:"",
        }
        this._handleTextFieldChange=this._handleTextFieldChange.bind(this)
        this.roomButtonPressed=this.roomButtonPressed.bind(this)
    }
    render(){
        return(
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <Image
                src="https://i.ibb.co/KDTzgg9/room-join2.png"
                />

                <Grid container spacing={3}>
                    <Grid item xs={12} align="center">
                        <Typography variant="h4" component="h4">
                            Join A Place
                        </Typography>

                    </Grid>
                    <Grid item xs={12} align="center">
                        <TextField
                        label="Place Code"
                        placeholder="Enter a Place Code"
                        value={this.state.roomCode}
                        variant="filled"
                        onChange={this._handleTextFieldChange}
                        color="primary"
                        ></TextField>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Button variant="contained" color="primary" onClick={this.roomButtonPressed}>
                            Enter Place
                        </Button>
                    </Grid>
                    <Grid item xs={12} align="center">
                        <Button variant="contained" color="primary" to="/" component={Link}>
                            Back
                        </Button>
                    </Grid>
                </Grid>
            </ThemeProvider>
        );
    }
    _handleTextFieldChange(e){
        this.setState({
            roomCode:e.target.value
        })
    }
    roomButtonPressed() {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            code: this.state.roomCode,
          }),
        };
        fetch("/api/join-room", requestOptions)
          .then((response) => {
            if (response.ok) {
              this.props.history.push(`/room/${this.state.roomCode}`);
            } else {
              this.setState({ error: "Room not found." });
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
}
