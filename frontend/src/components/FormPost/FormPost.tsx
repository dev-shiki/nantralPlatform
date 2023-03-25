import { Close } from '@mui/icons-material';
import {
  Alert,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  IconButton,
  useMediaQuery,
} from '@mui/material';
import axios from 'axios';
import * as React from 'react';
import { useTranslation } from 'react-i18next';
import { PostProps, postsToCamelCase } from '../../Props/Post';
import { theme } from '../style/palette';
import FormGroup, { FieldType } from '../../utils/form';
import { GroupProps } from '../../Props/Group';
import { ConfirmationModal } from '../Modal/ConfirmationModal';

export function FormPost(props: {
  mode?: 'create' | 'edit';
  open: boolean;
  onClose: () => void;
  post?: PostProps;
  onUpdate?: (post: PostProps) => void;
}) {
  const { open, onClose, post, onUpdate, mode } = props;
  const { t } = useTranslation('translation');
  const [values, setValues] = React.useState<PostProps>(
    post
      ? structuredClone(post)
      : { group: undefined, publicity: 'Pub', publicationDate: new Date() }
  );
  const [errors, setErrors] = React.useState<any>({});
  const [loading, setLoading] = React.useState<boolean>(false);
  const [adminGroup, setAdminGroup] = React.useState<Array<GroupProps>>([]);
  const [confirmationOpen, setConfirmationOpen] =
    React.useState<boolean>(false);
  const fullScreen: boolean = useMediaQuery(theme.breakpoints.down('md'));
  const defaultFields: FieldType[] = [
    {
      kind: 'select',
      label: t('form.group'),
      required: true,
      name: 'group',
      item: adminGroup?.map((group: GroupProps) => [
        group.name,
        group.id.toString(),
      ]),
      disabled: mode === 'edit',
    },
    {
      kind: 'text',
      name: 'title',
      label: t('form.PostTitle'),
      required: true,
      rows: 2,
    },
    {
      kind: 'richtext',
      label: t('form.description'),
      name: 'description',
    },
    {
      kind: 'datetime',
      name: 'publicationDate',
      label: t('form.publicationDate'),
      rows: 2,
      disablePast: true,
    },
    {
      kind: 'file',
      description: t('form.imageDescription'),
      label: t('form.image'),
      name: 'image',
    },
    {
      kind: 'select',
      name: 'publicity',
      label: t('form.publicity'),
      required: true,
      item: [
        [t('form.public'), 'Pub'],
        [t('form.membersOnly'), 'Mem'],
      ],
    },
    {
      kind: 'boolean',
      label: t('form.pinned'),
      name: 'pinned',
      rows: 1,
      type: 'checkbox',
    },
  ];

  React.useEffect(() => {
    setErrors({});
  }, [open]);

  React.useEffect(() => {
    axios
      .get('/api/group/group/', {
        params: { admin: true },
      })
      .then((res) => setAdminGroup(res.data.results));
  }, []);

  React.useEffect(() => {
    setValues(
      post
        ? structuredClone(post)
        : { group: undefined, publicity: 'Pub', publicationDate: new Date() }
    );
  }, [post]);

  const deletePost = () => {
    setLoading(true);
    axios
      .delete(`/api/post/${post.id}/`)
      .then(() => {
        onUpdate(null);
        onClose();
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setErrors(err.response.data);
        setLoading(false);
      });
  };
  const createPost = () => {
    const formData = new FormData();
    if (values.image && typeof values.image !== 'string')
      formData.append('image', values.image, values.image.name);
    if (values.group) formData.append('group', values.group.toString());
    formData.append('publicity', values.publicity);
    formData.append('title', values.title || '');
    console.log(values.description);
    formData.append('description', values.description || '<p></p>');
    if (values.pageSuggestion)
      formData.append('page_suggestion', values.pageSuggestion);
    formData.append('publication_date', values.publicationDate.toISOString());
    formData.append('pinned', values.pinned ? 'true' : 'false');
    axios
      .post(`/api/post/`, formData, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      })
      .then((res) => {
        postsToCamelCase([res.data]);
        onUpdate(res.data);
      })
      .then(() => {
        onClose();
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setErrors(err.response.data);
        setLoading(false);
      });
  };
  const updatePost = () => {
    setLoading(true);
    const formData = new FormData();
    // To avoid typescript error
    if (values.image && typeof values.image !== 'string')
      formData.append('image', values.image, values.image.name);

    if (values.group) formData.append('group', post.group.toString());
    formData.append('publicity', values.publicity);
    formData.append('title', values.title);
    formData.append('description', values.description || '<p></p>');
    if (values.pageSuggestion)
      formData.append('page_suggestion', values.pageSuggestion);
    formData.append('publication_date', values.publicationDate.toISOString());
    formData.append('pinned', values.pinned ? 'true' : 'false');
    axios
      .put(`/api/post/${post.id}/`, formData, {
        headers: {
          'content-type': 'multipart/form-data',
        },
      })
      .then((res) => {
        postsToCamelCase([res.data]);
        setValues(
          post
            ? structuredClone(post)
            : {
                group: undefined,
                publicity: 'Pub',
                publicationDate: new Date(),
              }
        );
        onUpdate(res.data);
      })
      .then(() => {
        onClose();
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setErrors(err.response.data);
        setLoading(false);
      });
  };
  return (
    <>
      <Dialog
        open={open}
        onClose={onClose}
        scroll="paper"
        fullWidth
        fullScreen={fullScreen}
        maxWidth="md"
        sx={{ margin: 0 }}
      >
        <DialogTitle
          id="scroll-dialog-title"
          sx={{
            width: '100%',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          {mode === 'edit' ? t('form.editPost') : t('form.createAPost')}
          <IconButton onClick={onClose}>
            <Close />
          </IconButton>
        </DialogTitle>
        <DialogContent
          dividers
          sx={{ display: 'flex', flexDirection: 'column' }}
        >
          {errors.non_field_errors &&
            errors.non_field_errors.map((text) => (
              <Alert variant="filled" severity="error" key={text}>
                {text}
              </Alert>
            ))}

          <div>
            <FormGroup
              fields={defaultFields}
              values={values}
              setValues={setValues}
              errors={errors}
            />
          </div>
          {mode === 'edit' && (
            <Button
              disabled={loading}
              color="warning"
              variant="outlined"
              onClick={() => setConfirmationOpen(true)}
            >
              {t('form.deletePost')}
            </Button>
          )}
        </DialogContent>
        <DialogActions style={{ justifyContent: 'right' }}>
          <div style={{ display: 'flex' }}>
            {mode === 'edit' ? (
              <>
                <Button
                  disabled={loading}
                  color="inherit"
                  variant="text"
                  onClick={onClose}
                  sx={{ marginRight: 1 }}
                >
                  {t('form.cancel')}
                </Button>
                <Button
                  disabled={loading}
                  color="info"
                  variant="contained"
                  onClick={updatePost}
                >
                  {t('form.editPost')}
                </Button>
              </>
            ) : (
              <Button
                type="submit"
                disabled={loading}
                color="info"
                variant="contained"
                onClick={createPost}
                sx={{ marginRight: 1 }}
              >
                {t('form.createPost')}
              </Button>
            )}
          </div>
        </DialogActions>
      </Dialog>
      <ConfirmationModal
        title={t('form.deletePost')}
        open={confirmationOpen}
        onClose={(value) => {
          if (value) deletePost();
          setConfirmationOpen(false);
        }}
        content={t('post.confirmDelete')}
      />
    </>
  );
}

FormPost.defaultProps = {
  mode: 'edit',
  post: null,
  onUpdate: () => null,
};
