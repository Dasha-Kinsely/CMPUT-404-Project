import React, { useState, useEffect } from "react";
import {
  Container,
  Grid,
  List,
  Button,
  Icon,
  Image,
  Modal
} from "semantic-ui-react";
import axios from "axios";
import {
  getAllUsers,
  getDefaultVisiblePosts
} from "../../ApiFetchers/getters/Axios";

const SplitContainer = () => {
  const [authorData, setAuthorData] = useState([]);
  const [postData, setPostData] = useState([]);
  const [authorLoading, setAuthorLoading] = useState(false);
  const [authorError, setAuthorError] = useState(false);
  const [postError, setPostError] = useState(false);
  const [postLoading, setPostLoading] = useState(false);
  useEffect(() => {
    const getAuthors = async () => {
      setAuthorError(false);
      setAuthorLoading(true);
      try {
        const authorFetcher = await getAllUsers(); //get data from api's url
        setAuthorData(authorFetcher.data);
      } catch (error) {
        setAuthorError(true);
      }
      setAuthorLoading(false);
    };
    const getPosts = async () => {
      setPostError(false);
      setPostLoading(true);
      try {
        const postFetcher = await getDefaultVisiblePosts();
        setPostData(postFetcher.data);
      } catch (error) {
        setPostError(true);
      }
      setPostLoading(false);
    };
    getPosts();
    getAuthors();
  }, []);
  const openContent = (e, content) => {
    e.preventDefault();
    console.log(content);
  };
  return (
    <Container textAlign="center">
      <Grid column={2} divided>
        <Grid.Row>
          <Grid.Column width={3}>
            <List.Header>
              <strong>Available Authors</strong>
            </List.Header>
            {authorError && (
              <List.Item>
                <List.Content>
                  <List.Description>Something went wrong ...</List.Description>
                </List.Content>
              </List.Item>
            )}
            {authorLoading ? (
              <List.Item>
                <List.Content>
                  <List.Description>Loading ...</List.Description>
                </List.Content>
              </List.Item>
            ) : (
              <List divided relaxed>
                {authorData.map(item => (
                  <List.Item key={item.id}>
                    <Image
                      avatar
                      src="https://react.semantic-ui.com/images/avatar/small/rachel.png"
                    />
                    <List.Content>
                      <List.Header>{item.username}</List.Header>
                      <Button animated size="tiny">
                        <Button.Content visible>Follow</Button.Content>
                        <Button.Content hidden>
                          <Icon name="arrow right" />
                        </Button.Content>
                      </Button>
                    </List.Content>
                  </List.Item>
                ))}
              </List>
            )}
          </Grid.Column>
          <Grid.Column width={13}>
            <List.Header>
              <strong>Posts I Can See</strong>
            </List.Header>
            {postError && (
              <List.Item>
                <List.Content>
                  <List.Description>Something went wrong ...</List.Description>
                </List.Content>
              </List.Item>
            )}
            {postLoading ? (
              <List.Item>
                <List.Content>
                  <List.Description>Loading ...</List.Description>
                </List.Content>
              </List.Item>
            ) : (
              <List divided relaxed>
                {postData.map(item => (
                  <List.Item key={item.id}>
                    <List.Content>
                      <Modal
                        trigger={
                          <List.Header
                            as="a"
                            onClick={e => {
                              openContent(e, item.content);
                            }}
                          >
                            {item.id}
                          </List.Header>
                        }
                      >
                        <Modal.Content>
                          <Modal.Description>{item.content}</Modal.Description>
                        </Modal.Content>
                      </Modal>
                      <List.Description>{item.author}</List.Description>
                      <List.Description>{item.mod_time}</List.Description>
                    </List.Content>
                  </List.Item>
                ))}
              </List>
            )}
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>
  );
};

export default SplitContainer;
