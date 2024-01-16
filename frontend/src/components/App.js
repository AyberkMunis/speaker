import React, {Component, component} from "react";
import {render} from "react-dom";
import HomePage  from "./HomePage";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import {BrowserRouter as Router, Switch,Redirect, Route} from "react-router-dom";
export default class App extends Component{
    constructor(props){
        super(props);
    }
    render(){
        return(<div className="center"><HomePage></HomePage></div>);
    }
}
const appDiv=document.getElementById("app");
render(<App />,appDiv);