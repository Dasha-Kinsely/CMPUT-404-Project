import React, { useState } from "react";
import {
  Button,
  Form,
  Grid,
  Container,
  Input,
  TextArea,
  Select
} from "semantic-ui-react";
const typeOptions = [
  {
    key: "plaintext",
    text: "Plain Text",
    value: "plaintext"
  },
  {
    key: "markdown",
    text: "Mark Down",
    value: "markdown"
  }
];
const visabilityOptions = [
  {
    key: "public",
    text: "Public",
    value: "public"
  },

  {
    key: "foaf",
    text: "FOAF",
    value: "foaf"
  },
  {
    key: "friends",
    text: "Friends",
    value: "friends"
  },

  {
    key: "friendsonhost",
    text: "Friends on My Host",
    value: "friendsonhost"
  },
  {
    key: "myself",
    text: "Myself",
    value: "myself"
  }
];
const NewPostForm = () => {
  const [ready, setReady] = useState(false);
  const [dataSet, setDataSet] = useState({
    title: "",
    category: "",
    description: "",
    contentType: "",
    content: "",
    origin: "",
    source: "",
    author: "",
    visibility: "",
    error: "",
    loading: false,
    redirecting: false
  });
  const handleSubmit = e => {
    e.preventDefault();
    setReady(true);
    console.log(dataSet);
  };
  const handleInput = name => event => {
    //simply sets the states using input value as user types
    setDataSet({ ...dataSet, [name]: event.target.value });
  };
  var contentSelect = dataSet.contentType;
  const handleTypeSelect = (e, { value }) => {
    setDataSet({ ...dataSet, contentType: value });
  };
  var visSelect = dataSet.visibility;
  const handleVisibilitySelect = (e, { value }) => {
    setDataSet({ ...dataSet, visibility: value });
  };
  return (
    <Container>
      <Grid.Row>
        <Grid.Column>
          <Form>
            <Form.Group widths="equal">
              <Form.Field
                required
                id="post-title"
                control={Input}
                onChange={handleInput("title")}
                label="Title"
                placeholder="Title"
              />
              <Form.Group width="equal">
                <Form.Field
                  required
                  id="post-category"
                  control={Input}
                  onChange={handleInput("category")}
                  label="Category"
                  placeholder="Category"
                />
                <Form.Field
                  required
                  id="post-contentType"
                  control={Select}
                  options={typeOptions}
                  onChange={handleTypeSelect}
                  selection
                  value={contentSelect}
                  label="Content Type"
                  placeholder="Content Type"
                />
              </Form.Group>
            </Form.Group>
            <Form.Field
              id="post-description"
              control={TextArea}
              onChange={handleInput("description")}
              label="Description"
              placeholder="Description"
              style={{ maxHeight: "60px" }}
            />
            <Form.Field
              required
              id="post-Content"
              control={TextArea}
              label="Content"
              placeholder="Content"
              onChange={handleInput("content")}
              style={{ minHeight: "180px" }}
            />
            <Form.Group widths="equal">
              <Form.Field
                id="post-source"
                control={Input}
                onChange={handleInput("source")}
                label="Source"
                placeholder="Source"
              />
              <Form.Field
                id="post-origin"
                control={Input}
                label="Origin"
                onChange={handleInput("origin")}
                placeholder="Origin"
              />
            </Form.Group>
            <Form.Group width="equal">
              <Form.Field
                required
                id="post-visibility"
                control={Select}
                options={visabilityOptions}
                onChange={handleVisibilitySelect}
                selection
                value={visSelect}
                label="Visible To"
              />
              <Button
                color="blue"
                fluid
                size="small"
                onClick={e => {
                  handleSubmit(e);
                }}
              >
                OK
              </Button>
            </Form.Group>
          </Form>
        </Grid.Column>
      </Grid.Row>
    </Container>
  );
};

export default NewPostForm;
