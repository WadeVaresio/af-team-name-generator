import React, {useState} from "react";
import {Button, ButtonToolbar, ButtonGroup} from "@appfolio/react-gears";
import {List} from "@appfolio/react-gears";
import {Input, Form} from "@appfolio/react-gears";

const SearchField = () => {
    const [name, setName] = useState();
    const [puns, setPuns] = useState();

    const getResults = () => {
        // const url = `/generate/non_recursive?input=${name}`;
        const url = `https://af-team-name-generator-backend.herokuapp.com/generate/non_recursive?input=${name}`;

        fetch(url).then((response) => {
            return response.json();
        }).then( (data) => {
            let set = new Set();
            data.forEach( (element) => set.add(element))
            setPuns(Array.from(set));
        }).catch( (e) => console.log(e));
    };

    const getRandom = () => {
        const url = `/random_name`;

        fetch(url).then((response) => {
            return response.json();
        }).then( (data) => {
            setName(data.original)

            let set = new Set();
            data.puns.forEach( (element) => set.add(element))
            setPuns(Array.from(set));
        }).catch( (e) => console.log(e));
    };

    const onSubmit = (event) => {
        event.preventDefault();
        getResults();
    };

    const styling = {
        "margin-top": '10px',
        "margin-bottom": '30px'
    };

    const styling2 = {
        "margin-top": '10px',
        "margin-bottom": '30px',
        "margin-left": '15px'
    };

    return(
        <div className={"title"}>

            <Form onSubmit={onSubmit}>
                <Input placeholder="Enter Original Name: " id="hello"
                       onSubmit={onSubmit}
                       onChange={(event) => setName(event.target.value)}
                       value={name}
                />
            </Form>

            <div className={"container"}>
                <ButtonToolbar>
                    <Button onClick={getResults} color={"primary"} style={styling}>Generate Names</Button>
                    <Button onClick={getRandom} color={"secondary"} style={styling2} size={"md"}>I'm Feeling Lucky</Button>
                </ButtonToolbar>
            </div>

            <List
                height={'40vh'}
                items={puns}
                striped={true}
                flush={false}
                >
                {(item) =>
                    <h5>
                        {item}
                    </h5>
                }
            </List>
        </div>
    )
};

export default SearchField;